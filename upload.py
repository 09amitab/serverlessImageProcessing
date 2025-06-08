import json
import boto3
import base64
import uuid
import os

s3 = boto3.client('s3')
bucket = os.environ['BUCKET_NAME']

def lambda_handler(event, context):
    try:
        body = json.loads(event['body'])
        image_data = base64.b64decode(body['image'])
        file_name = f"{uuid.uuid4()}.jpg"

        s3.put_object(Bucket=bucket, Key=file_name, Body=image_data)

        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "Content-Type",
                "Access-Control-Allow-Methods": "POST,OPTIONS"
            },
            "body": json.dumps({"message": "Upload successful", "file": file_name})
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
