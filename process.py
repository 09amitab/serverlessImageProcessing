import boto3
import os
import json

sns = boto3.client('sns')
topic_arn = os.environ['SNS_TOPIC_ARN']

def lambda_handler(event, context):
    for record in event['Records']:
        key = record['s3']['object']['key']
        bucket = record['s3']['bucket']['name']
        message = f"Image {key} uploaded to bucket {bucket} has been processed."

        sns.publish(
            TopicArn=topic_arn,
            Subject="Image Processed",
            Message=message
        )

    return {"statusCode": 200, "body": "Processed and notified."}
