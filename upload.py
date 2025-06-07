import boto3
import base64
import uuid
import os

s3 = boto3.client('s3')
bucket_name = os.environ['BUCKET_NAME']

def lambda_handler(event, context):
    try:
        content_type = event["headers"].get("content-type") or event["headers"].get("Content-Type")
        if "multipart/form-data" not in content_type:
            return {"statusCode": 400, "body": "Invalid content type"}

        image_data = base64.b64decode(event["body"])
        filename = f"{uuid.uuid4()}.jpg"

        s3.put_object(
            Bucket=bucket_name,
            Key=filename,
            Body=image_data,
            ContentType='image/jpeg'
        )

        return {
            "statusCode": 200,
            "body": f"Image uploaded as {filename}"
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": f"Error: {str(e)}"
        }
