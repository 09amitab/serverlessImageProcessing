import boto3
import base64
import os
import json

s3 = boto3.client('s3')

ALLOWED_EXTENSIONS = ['jpg', 'jpeg', 'png']
BUCKET_NAME = os.environ['BUCKET_NAME']

def lambda_handler(event, context):
    try:
        # Parse base64-encoded image from body
        body = json.loads(event['body'])
        image_data = base64.b64decode(body['file'])
        filename = body['filename']

        # Validate file extension
        ext = filename.split('.')[-1].lower()
        if ext not in ALLOWED_EXTENSIONS:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Invalid file type. Only jpg, jpeg, png allowed."})
            }

        # Upload to S3
        s3.put_object(
            Bucket=BUCKET_NAME,
            Key=filename,
            Body=image_data,
            ContentType=f"image/{ext}"
        )

        return {
            "statusCode": 200,
            "body": json.dumps({"message": "File uploaded successfully", "filename": filename})
        }

    except Exception as e:
        print("Error:", str(e))
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "Internal server error", "details": str(e)})
        }
