import json
import boto3
import os

sns = boto3.client('sns')
topic_arn = os.environ['TOPIC_ARN']

def lambda_handler(event, context):
    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        key = record['s3']['object']['key']

        message = f"Image {key} uploaded to bucket {bucket} was processed."
        print(message)

        sns.publish(
            TopicArn=topic_arn,
            Message=message,
            Subject="Image Processing Notification"
        )
