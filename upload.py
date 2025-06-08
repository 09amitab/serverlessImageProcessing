import json
import boto3
import base64
import os

s3 = boto3.client('s3')

def lambda_handler(event, context):
    # Handle CORS preflight
    if event.get('httpMethod') == 'OPTIONS':
        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "Content-Type",
                "Access-Control-Allow-Methods": "OPTIONS,POST"
            },
            "body": json.dumps({"message": "CORS preflight successful"})
        }

    try:
        body = json.loads(event.get('body') or '{}')

        if 'image' not in body:
            raise ValueError("Missing 'image' field in request body")

        image_data = body['image']
        filename = body.get('filename', 'uploaded_image.jpg')

        image_content = base64.b64decode(image_data.split(",")[1])
        bucket_name = os.environ['BUCKET_NAME']

        s3.put_object(Bucket=bucket_name, Key=filename, Body=image_content, ContentType="image/jpeg")

        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "Content-Type",
                "Access-Control-Allow-Methods": "OPTIONS,POST"
            },
            "body": json.dumps({"message": "Upload successful", "filename": filename})
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "Content-Type",
                "Access-Control-Allow-Methods": "OPTIONS,POST"
            },
            "body": json.dumps({"error": str(e)})
        }
