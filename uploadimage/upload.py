import json
import boto3
import base64
import os
import logging

from urllib.parse import unquote_plus

s3 = boto3.client('s3')
logger = logging.getLogger()
logger.setLevel(logging.INFO)

BUCKET_NAME = os.environ.get('BUCKET_NAME', '')

def lambda_handler(event, context):
    logger.info("Received event: %s", json.dumps(event))

    try:
        if event['httpMethod'] != 'POST':
            return _response(405, "Method Not Allowed")

        content_type = event['headers'].get('Content-Type') or event['headers'].get('content-type')

        # Check multipart form-data
        if not content_type or not content_type.startswith("multipart/form-data"):
            return _response(400, "Invalid content type")

        # Extract file content from the body using base64 (API Gateway handles the decoding)
        body = base64.b64decode(event['body']) if event.get("isBase64Encoded", False) else event['body']
        
        # Naively extract file content and name
        file_content = body.split(b"\r\n\r\n", 1)[1].rsplit(b"\r\n", 2)[0]
        header_line = body.split(b"\r\n", 2)[1].decode()
        file_name = header_line.split("filename=")[1].strip('"')

        # Upload to S3
        s3.put_object(
            Bucket=BUCKET_NAME,
            Key=file_name,
            Body=file_content,
            ContentType="image/jpeg" if file_name.endswith(".jpg") or file_name.endswith(".jpeg") else "image/png"
        )

        return _response(200, f"Image '{file_name}' uploaded successfully.")

    except Exception as e:
        logger.exception("Error uploading image")
        return _response(500, f"Error uploading image: {str(e)}")


def _response(status_code, message):
    return {
        "statusCode": status_code,
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "POST, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type",
            "Content-Type": "application/json"
        },
        "body": json.dumps({"message": message})
    }

    

