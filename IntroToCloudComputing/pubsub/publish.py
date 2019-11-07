import os
#to import that, use pip install google-cloud-pubsub
# or, go to settings and add package google-cloud-pubsub
from google.cloud import pubsub_v1

# you need to change this path and file name. See to get file, follow the steps here https://cloud.google.com/video-intelligence/docs/common/auth
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="D:/gcpFun/mycreds.json"

# you need to update this with youyr project id
project_id = 'qwiklabs-gcp-00-9300da392434'


publisher = pubsub_v1.PublisherClient()
# be sure that the topic name matches what you use in the subscriber code
topic_name = 'projects/{project_id}/topics/{topic}'.format(
    project_id='qwiklabs-gcp-00-9300da392434',
    topic='myTopic2',  # Set this to something appropriate.
)

# Make topic. Include this line only once. After running the first time, comment this line out
#publisher.create_topic(topic_name)


publisher.publish(topic_name, b'My first message3!', spam='eggs')