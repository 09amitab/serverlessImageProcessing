import json
import base64
import boto3
import os
from datetime import datetime

s3 = boto3.client('s3')
bucket_name = os.environ['BUCKET_NAME']

def lambda_handler(event, context):
    try:
        if event.get("isBase64Encoded"):
            file_content = base64.b64decode(event['body'])
        else:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Expected base64-encoded data"})
            }

        headers = event.get("headers", {})
        content_type = headers.get("Content-Type") or headers.get("content-type")

        if not content_type:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Missing Content-Type header"})
            }

        extension = "jpg" if "jpeg" in content_type else "png" if "png" in content_type else None

        if not extension:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Unsupported image format"})
            }

        filename = f"image_{datetime.utcnow().strftime('%Y%m%d%H%M%S%f')}.{extension}"
        s3.put_object(Bucket=bucket_name, Key=filename, Body=file_content, ContentType=content_type)

        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "Content-Type",
                "Access-Control-Allow-Methods": "POST,OPTIONS"
            },
            "body": json.dumps({"message": "Image uploaded", "filename": filename})
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
