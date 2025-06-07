import json
import boto3
import os

sns = boto3.client('sns')
SNS_TOPIC_ARN = os.environ['SNS_TOPIC_ARN']

def lambda_handler(event, context):
    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        key = record['s3']['object']['key']

        message = f"New image uploaded: s3://{bucket}/{key}"
        
        # Publish to SNS
        sns.publish(
            TopicArn=SNS_TOPIC_ARN,
            Message=message,
            Subject="Image Upload Notification"
        )
        
        print(message)

    return {
        "statusCode": 200,
        "body": json.dumps({"message": "SNS notification sent"})
    }
