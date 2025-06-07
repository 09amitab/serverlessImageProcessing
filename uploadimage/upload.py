import boto3
import base64
import os
import json

s3 = boto3.client('s3')
ALLOWED_EXTENSIONS = ['jpg', 'jpeg', 'png']
BUCKET_NAME = os.environ['BUCKET_NAME']

def lambda_handler(event, context):
    # CORS Preflight request
    if event.get("httpMethod") == "OPTIONS":
        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",  # Previously blank, must be '*'
                "Access-Control-Allow-Headers": "Content-Type",
                "Access-Control-Allow-Methods": "POST,OPTIONS"
            },
            "body": json.dumps("CORS preflight OK")
        }

    try:
        if 'body' not in event:
            raise ValueError("Request body is missing")

        body = json.loads(event['body'])

        if 'file' not in body or 'filename' not in body:
            raise ValueError("Missing 'file' or 'filename' in request")

        image_data = base64.b64decode(body['file'])
        filename = body['filename']

        ext = filename.split('.')[-1].lower()
        if ext not in ALLOWED_EXTENSIONS:
            return {
                "statusCode": 400,
                "headers": cors_headers(),
                "body": json.dumps({"error": "Invalid file type. Only jpg, jpeg, png allowed."})
            }

        s3.put_object(
            Bucket=BUCKET_NAME,
            Key=filename,
            Body=image_data,
            ContentType=f"image/{ext}"
        )

        return {
            "statusCode": 200,
            "headers": cors_headers(),
            "body": json.dumps({"message": "Upload successful", "filename": filename})
        }

    except Exception as e:
        print("Upload Error:", str(e))
        return {
            "statusCode": 500,
            "headers": cors_headers(),
            "body": json.dumps({"error": "Internal server error", "details": str(e)})
        }

def cors_headers():
    return {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Headers": "Content-Type",
        "Access-Control-Allow-Methods": "POST,OPTIONS"
    }
