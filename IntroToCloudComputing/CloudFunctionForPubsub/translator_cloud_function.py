import base64
import json
import os
import logging
from google.cloud import pubsub_v1
import google.auth


def hello_pubsub(event, context):
    """Triggered from a message on a Cloud Pub/Sub topic.
    Args:
         event (dict): Event payload.
         context (google.cloud.functions.Context): Metadata for the event.
    """
    pubsub_message = base64.b64decode(event['data']).decode('utf-8')
    print(pubsub_message)

    _, PROJECT_ID = google.auth.default()
    OUTPUT_TOPIC_NAME = "OutputTopic"
    publisher = pubsub_v1.PublisherClient()
    output_topic_full_name = 'projects/{project_id}/topics/{topic}'.format(
    	project_id=PROJECT_ID,
    	topic=OUTPUT_TOPIC_NAME,)
    publisher.publish(output_topic_full_name,  base64.b64decode(event['data']), spam='eggs')
