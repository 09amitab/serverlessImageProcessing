import boto3
import os
import json
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

sns = boto3.client('sns')
topic_arn = os.environ['TOPIC_ARN']

def lambda_handler(event, context):
    try:
        for record in event['Records']:
            s3_info = record['s3']
            bucket = s3_info['bucket']['name']
            key = s3_info['object']['key']

            message = f"Image uploaded: s3://{bucket}/{key}"
            logger.info(message)

            sns.publish(
                TopicArn=topic_arn,
                Subject="New Image Uploaded",
                Message=message
            )

        return {
            "statusCode": 200,
            "body": json.dumps({"message": "Notification sent"})
        }

    except Exception as e:
        logger.error("Error: %s", e)
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
