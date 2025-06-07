import json
import boto3
import os

sns = boto3.client("sns")
topic_arn = os.environ["SNS_TOPIC_ARN"]

def lambda_handler(event, context):
    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        key = record['s3']['object']['key']

        message = f"New image uploaded: s3://{bucket}/{key}"
        print("Sending SNS:", message)

        sns.publish(
            TopicArn=topic_arn,
            Subject="New Image Uploaded",
            Message=message
        )

    return {"statusCode": 200}
