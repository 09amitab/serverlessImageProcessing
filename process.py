import json
import boto3
import os

sns = boto3.client('sns')
topic_arn = os.environ['TOPIC_ARN']

def lambda_handler(event, context):
    for record in event['Records']:
        key = record['s3']['object']['key']
        message = f"Image uploaded and processed: {key}"

        sns.publish(TopicArn=topic_arn, Message=message, Subject="Image Processed")

    return {"statusCode": 200, "body": json.dumps("Processed")}
