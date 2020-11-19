# to debug on your laptop, you must set
#               set the location of GCP credentials json file
#               set this with your project id
# to run in GKE, you must
#               set GOOGLE_APPLICATION_CREDENTIALS with gke secrets (see tutorial)
import json
import os
import logging
#to import that, use pip install google-cloud-pubsub
# or, go to settings and add package google-cloud-pubsub
from google.cloud import pubsub_v1
import google.auth

# you need to change this path and file name. See to get file, follow the steps here https://cloud.google.com/video-intelligence/docs/common/auth
if "GOOGLE_APPLICATION_CREDENTIALS" not in os.environ:
    # for debugging on your laptop
    # you need to set the location of GCP credentials json file
    if os.path.isfile("D:/gcpFun/mycreds.json"):
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="D:/gcpFun/mycreds.json"
    else:
        # handle docker case
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "mycreds.json"
#else: # this is running on GCP where you need to use gke secrets to put the gcp credentials into os.environ["GOOGLE_APPLICATION_CREDENTIALS"]

# detect if running on kubernetes
# note, if the pubsub is in a differnet project, then you need to force this condition to always be False (change the text "True" to "False")
if True and "KUBERNETES_PORT_53_UDP_ADDR" in os.environ:    # kubernetes always has KUBERNETES_PORT_53_UDP_ADDR defined
    # is running in kubernetes
    # get project id
    _, PROJECT_ID = google.auth.default()
else:
    # not running in k8 (debugging on your laptop)
    # you need to set this with your project id
    PROJECT_ID = 'qwiklabs-gcp-00-e079a656304a'

# be sure that the topic name matches what you use in the subscriber code
OUTPUT_TOPIC_NAME = "OutputTopic"  # Set this to something appropriate.
INPUT_TOPIC_NAME = "InputTopic"
INPUT_SUBSCRIPTION_NAME = 'MyTranslationSub'

publisher = pubsub_v1.PublisherClient()

output_topic_full_name = 'projects/{project_id}/topics/{topic}'.format(
    project_id=PROJECT_ID,
    topic=OUTPUT_TOPIC_NAME,
)

input_topic_full_name = 'projects/{project_id}/topics/{topic}'.format(
    project_id=PROJECT_ID,
    topic=INPUT_TOPIC_NAME,
)

input_subscription_full_name = 'projects/{project_id}/subscriptions/{sub}'.format(
    project_id=PROJECT_ID,
    sub=INPUT_SUBSCRIPTION_NAME,  # Set this to something appropriate.
)

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
log = logging.getLogger(__file__) # set the name of the log entry



# check if topic already exists. If not, then create it
fd = False
"""
# loop through each topic. It is better to use a List Comprehensions, shown below
for topic in publisher.list_topics(project="projects/{}".format(PROJECT_ID)):
    print(topic)
    if topic.name == output_topic_full_name:
        fd = True
        break
"""

if output_topic_full_name in [t.name for t in publisher.list_topics(project="projects/{}".format(PROJECT_ID))]:
    fd = True
if fd==False:
    log.info("Did not find topic. Creating")
    publisher.create_topic(output_topic_full_name)
    log.info("Created Topic {}".format(output_topic_full_name))


# check if input topic already exists. If not, then create it
if input_topic_full_name not in [t.name for t in publisher.list_topics(project="projects/{}".format(PROJECT_ID))]:
    # need to make input topic
    log.info("Did not find topic. Creating")
    publisher.create_topic(input_topic_full_name)
    log.info("Created Topic {}".format(input_topic_full_name))

# Make subscriber object
subscriber = pubsub_v1.SubscriberClient()

# make subscription if needed
if input_subscription_full_name not in [t.name for t in subscriber.list_subscriptions(project="projects/{}".format(PROJECT_ID))]:
    log.info("Did not find subscription. Creating")
    # Make subscription. Include this line only once. After running the first time, comment this line out
    subscriber.create_subscription(name=input_subscription_full_name, topic=input_topic_full_name, ack_deadline_seconds = 60)
    log.info("Created subscription {}".format(input_subscription_full_name))

# Define where to pull messages
subscription_path = subscriber.subscription_path(PROJECT_ID, INPUT_SUBSCRIPTION_NAME)

# Set how many messages to pull in a bunch
NUM_MESSAGES = 1
while True:
    try:
        # Pull the specfied number of messages.
        response = subscriber.pull(subscription=subscription_path, max_messages=NUM_MESSAGES, timeout = 30)

        # Consume messages
        ack_ids = []
        for received_message in response.received_messages:
            ack_ids.append(received_message.ack_id)
            subscriber.modify_ack_deadline(subscription=subscription_path, ack_ids=ack_ids, ack_deadline_seconds=60) # extend deadline for this message for 60 seconds from now
            log.info("Received: {} with id {}".format(received_message.message.data, received_message.ack_id))
            try:
                res_dict = json.loads(received_message.message.data.decode('utf-8'))
            except:
                log.info("message is not json")
            publisher.publish(output_topic_full_name, received_message.message.data, spam='eggs')


        if len(ack_ids)>0:
            # Acknowledge all of the received messages so they will not be sent again.
            subscriber.acknowledge(request={"subscription": subscription_path, "ack_ids": ack_ids})
        else:
            print("timed out. Re-requesting messages")
    except google.api_core.exceptions.GoogleAPICallError as err:
        log.info("error: {0}".format(err))


log.info("done")