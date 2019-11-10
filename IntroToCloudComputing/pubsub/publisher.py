import os
#to import that, use pip install google-cloud-pubsub
# or, go to settings and add package google-cloud-pubsub
from google.cloud import pubsub_v1

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="D:/gcpFun/mycreds.json"

PROJECT_ID = 'qwiklabs-gcp-00-b5fcde6c3cb0'

TOPIC_NAME = 'myTopic'  # Set this to something appropriate.

topic_full_name = 'projects/{project_id}/topics/{topic}'.format(
    project_id=PROJECT_ID,
    topic=TOPIC_NAME,
)

# Make publisher object
publisher = pubsub_v1.PublisherClient()

# Make topic. Include this line only once. After running the first time, comment this line out
publisher.create_topic(topic_full_name)

# Send a message
publisher.publish(topic_full_name, b'My first message!', spam='eggs')
print("Sent first")
publisher.publish(TOPIC_NAME, b'My second message!', spam='eggs')
print("Sent second")