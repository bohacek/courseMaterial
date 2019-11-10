import os
#to import that, use pip install google-cloud-pubsub
# or, go to settings and add package google-cloud-pubsub
from google.cloud import pubsub_v1

# you need to set the location of GCP credentials json file
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="D:/gcpFun/mycreds.json"

# you need to set your project id
PROJECT_ID = 'qwiklabs-gcp-00-b5fcde6c3cb0'

TOPIC_NAME = 'myTopic'  # Set this to something, but be sure that it matches the topic name used in the publisher code.

SUBSCRIPTION_NAME = 'MySub' # set this to anything

topic_full_name = 'projects/{project_id}/topics/{topic}'.format(
    project_id=PROJECT_ID,
    topic=TOPIC_NAME,  # Set this to something appropriate.
)
subscription_full_name = 'projects/{project_id}/subscriptions/{sub}'.format(
    project_id=PROJECT_ID,
    sub=SUBSCRIPTION_NAME,  # Set this to something appropriate.
)

# Make subscriber object
subscriber = pubsub_v1.SubscriberClient()

# Make subscription. Include this line only once. After running the first time, comment this line out
subscriber.create_subscription(name=subscription_full_name, topic=topic_full_name)

# Define where to pull messages
subscription_path = subscriber.subscription_path(PROJECT_ID, SUBSCRIPTION_NAME)

# Set how many messages to pull in a bunch
NUM_MESSAGES = 1
# Pull the specfied number of messages.
response = subscriber.pull(subscription_path, max_messages=NUM_MESSAGES)

# Consume messages
ack_ids = []
for received_message in response.received_messages:
    print("Received: {} with id {}".format(received_message.message.data, received_message.ack_id))
    ack_ids.append(received_message.ack_id)

# Acknowledge all of the received messages so they will not be sent again.
subscriber.acknowledge(subscription_path, ack_ids)

print('Received and acknowledged {} messages. Done.'.format(len(response.received_messages)))


