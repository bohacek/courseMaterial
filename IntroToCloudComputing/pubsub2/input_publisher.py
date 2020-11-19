import os
import json
import time
#to import that, use pip install google-cloud-pubsub
# or, go to settings and add package google-cloud-pubsub
from google.cloud import pubsub_v1

# you need to set the location of GCP credentials json file
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="D:/gcpFun/mycreds.json"

# you need to set your project id
PROJECT_ID = 'qwiklabs-gcp-00-e079a656304a'

INPUT_TOPIC_NAME = 'InputTopic' # Set this to something, but be sure that it matches the topic name used in the subscriber code.

input_topic_full_name = 'projects/{project_id}/topics/{topic}'.format(
    project_id=PROJECT_ID,
    topic=INPUT_TOPIC_NAME,
)

# Make publisher object
publisher = pubsub_v1.PublisherClient()


# check if input topic already exists. If not, then create it
if input_topic_full_name not in [t.name for t in publisher.list_topics(project="projects/{}".format(PROJECT_ID))]:
    # need to make input topic
    print("Did not find topic. Creating")
    publisher.create_topic(input_topic_full_name)
    print("Created Topic {}".format(input_topic_full_name))


# Send a message
publisher.publish(input_topic_full_name, b'My first message!', spam='eggs') # note that the message starts with b. This converts the string to a byte string (as oppose to a python string)
print("Sent first")
cnt = 0
while True:
    publisher.publish(input_topic_full_name, json.dumps({"message":"My new message!","count":str(cnt)}).encode('utf-8'), spam='eggs')
    print("Sent {}".format(cnt))
    cnt += 1
    time.sleep(30)