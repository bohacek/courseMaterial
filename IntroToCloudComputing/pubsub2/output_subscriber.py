# to debug on your laptop, you must set
#               set the location of GCP credentials json file
#               set this with your project id
# to run in GKE, you must
#               set GOOGLE_APPLICATION_CREDENTIALS with gke secrets (see tutorial)
import json
import os
#to import that, use pip install google-cloud-pubsub
# or, go to settings and add package google-cloud-pubsub
from google.cloud import pubsub_v1
import google.auth

# you need to change this path and file name. See to get file, follow the steps here https://cloud.google.com/video-intelligence/docs/common/auth
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="D:/gcpFun/mycreds.json"

PROJECT_ID = 'qwiklabs-gcp-00-e079a656304a'

# be sure that the topic name matches what you use in the subscriber code
OUTPUT_TOPIC_NAME = "OutputTopic"  # Set this to something appropriate.
OUTPUT_SUBSCRIPTION_NAME = 'MyOutputSub'

subscriber = pubsub_v1.SubscriberClient()

output_topic_full_name = 'projects/{project_id}/topics/{topic}'.format(
    project_id=PROJECT_ID,
    topic=OUTPUT_TOPIC_NAME,
)

output_subscription_full_name = 'projects/{project_id}/subscriptions/{sub}'.format(
    project_id=PROJECT_ID,
    sub=OUTPUT_SUBSCRIPTION_NAME,  # Set this to something appropriate.
)

# check if output topic already exists. If not, then create it
publisher = pubsub_v1.PublisherClient() # we need a publisher object because only publishers can get the list of topics and create topics
if output_topic_full_name not in [t.name for t in publisher.list_topics(project="projects/{}".format(PROJECT_ID))]:
    print("Did not find topic. Creating")
    publisher.create_topic(output_topic_full_name)
    print("Created Topic {}".format(output_topic_full_name))


# make subscription if needed
if output_subscription_full_name not in [t.name for t in subscriber.list_subscriptions(project="projects/{}".format(PROJECT_ID))]:
    print("Did not find subscription. Creating")
    # Make subscription. Include this line only once. After running the first time, comment this line out
    subscriber.create_subscription(name=output_subscription_full_name, topic=output_topic_full_name, ack_deadline_seconds = 60)
    print("Created subscription {}".format(output_subscription_full_name))

# Define where to pull messages
subscription_path = subscriber.subscription_path(PROJECT_ID, OUTPUT_SUBSCRIPTION_NAME)

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
            print("Received: {} with id {}".format(received_message.message.data, received_message.ack_id))
            try:
                res_dict = json.loads(received_message.message.data.decode('utf-8'))
            except:
                print("message is not json")

        if len(ack_ids)>0:
            # Acknowledge all of the received messages so they will not be sent again.
            subscriber.acknowledge(request={"subscription": subscription_path, "ack_ids": ack_ids})
        else:
            print("timed out. Re-requesting messages")
    except google.api_core.exceptions.GoogleAPICallError as err:
        print("error: {0}".format(err))


print("done")