import boto3
import os
import base64
from urllib.parse import parse_qs

s3 = boto3.client("s3")
bucket = os.environ['BUCKET_NAME']

def lambda_handler(event, context):
    try:
        body = base64.b64decode(event["body"])
        filename = event["headers"].get("file-name", "uploaded-image.jpg")

        s3.put_object(
            Bucket=bucket,
            Key=filename,
            Body=body,
            ContentType=event["headers"].get("Content-Type", "image/jpeg")
        )

        return {
            "statusCode": 200,
            "body": f"Image '{filename}' uploaded successfully!"
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": f"Upload failed: {str(e)}"
        }
