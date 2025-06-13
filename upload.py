import boto3
import base64
import uuid
import os
import json

s3 = boto3.client('s3')
sns = boto3.client('sns')

BUCKET_NAME = os.environ['BUCKET_NAME']
TOPIC_ARN = os.environ['TOPIC_ARN']

def lambda_handler(event, context):
    try:
        body = event.get("body")
        is_base64_encoded = event.get("isBase64Encoded", False)

        if is_base64_encoded:
            image_data = base64.b64decode(body)
        else:
            image_data = body.encode('utf-8')

        image_id = str(uuid.uuid4())
        key = f"uploads/{image_id}.jpg"

        s3.put_object(Bucket=BUCKET_NAME, Key=key, Body=image_data, ContentType='image/jpeg')

        # Send SNS notification
        sns.publish(
            TopicArn=TOPIC_ARN,
            Subject="Image Uploaded",
            Message=f"A new image has been uploaded with ID: {image_id}"
        )

        return {
            "statusCode": 200,
            "body": json.dumps({"message": "Image uploaded successfully", "image_id": image_id}),
            "headers": {"Content-Type": "application/json"}
        }

    except Exception as e:
        print(f"Error: {e}")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)}),
            "headers": {"Content-Type": "application/json"}
        }
