import os
#to import that, use pip install google-cloud-pubsub
# or, go to settings and add package google-cloud-pubsub
from google.cloud import pubsub_v1

# you need to change this path and file name. See to get file, follow the steps here https://cloud.google.com/video-intelligence/docs/common/auth
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="D:/gcpFun/mycreds.json"

# you need to update this with youyr project id
project_id = 'qwiklabs-gcp-00-9300da392434'

# feel free to change this name
subscription_short_name='MY_SUBSCRIPTION_NAME'

subscriber = pubsub_v1.SubscriberClient()

# be sure the topic name here matches the topic name you made
topic_name = 'projects/{project_id}/topics/{topic}'.format(
    project_id=project_id,
    topic='myTopic2',  # Set this to something appropriate.
)
subscription_name = 'projects/{project_id}/subscriptions/{sub}'.format(
    project_id=project_id,
    sub=subscription_short_name,  # Set this to something appropriate.
)

# Make subscriptiuon. Include this line only once. After running the first time, comment this line out
subscriber.create_subscription(    name=subscription_name, topic=topic_name)


subscription_path = subscriber.subscription_path(project_id, subscription_short_name)

NUM_MESSAGES = 1

# The subscriber pulls a specific number of messages.
response = subscriber.pull(subscription_path, max_messages=NUM_MESSAGES)

ack_ids = []
for received_message in response.received_messages:
    print("Received: {}".format(received_message.message.data))
    ack_ids.append(received_message.ack_id)

# Acknowledges the received messages so they will not be sent again.
subscriber.acknowledge(subscription_path, ack_ids)

print('Received and acknowledged {} messages. Done.'.format(len(response.received_messages)))


