import json
import boto3
import os
import uuid

s3 = boto3.client('s3')
bucket = os.environ['BUCKET_NAME']

def lambda_handler(event, context):
    try:
        content_type = event["headers"].get("content-type") or event["headers"].get("Content-Type")
        if "multipart/form-data" not in content_type:
            return {
                "statusCode": 400,
                "body": "Only multipart/form-data supported",
                "headers": {
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Headers": "*",
                    "Access-Control-Allow-Methods": "POST,OPTIONS"
                }
            }

        filename = f"{uuid.uuid4()}.jpg"
        file_content = event['body']  # Assuming binary media enabled
        s3.put_object(Bucket=bucket, Key=filename, Body=file_content)

        return {
            "statusCode": 200,
            "body": json.dumps({"message": "Upload successful", "filename": filename}),
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "*",
                "Access-Control-Allow-Methods": "POST,OPTIONS"
            }
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": str(e),
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "*",
                "Access-Control-Allow-Methods": "POST,OPTIONS"
            }
        }
