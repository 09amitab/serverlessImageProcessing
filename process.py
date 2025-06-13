import boto3
import os
import json

s3 = boto3.client('s3')
sns = boto3.client('sns')

TOPIC_ARN = os.environ['TOPIC_ARN']

def lambda_handler(event, context):
    try:
        for record in event['Records']:
            bucket = record['s3']['bucket']['name']
            key = record['s3']['object']['key']

            print(f"Processing file: {key} from bucket: {bucket}")

            # (Optional) Download or process the file here
            response = s3.get_object(Bucket=bucket, Key=key)
            content = response['Body'].read()

            # Example: Just log file size
            print(f"File size: {len(content)} bytes")

            # Publish SNS notification
            sns.publish(
                TopicArn=TOPIC_ARN,
                Subject="Image Processed",
                Message=f"The image {key} has been processed."
            )

        return {"statusCode": 200, "body": "Success"}

    except Exception as e:
        print(f"Error processing image: {e}")
        return {"statusCode": 500, "body": json.dumps({"error": str(e)})}
