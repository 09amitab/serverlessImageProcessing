import boto3
import base64
import os
import json

s3 = boto3.client('s3')

ALLOWED_EXTENSIONS = ['jpg', 'jpeg', 'png']
BUCKET_NAME = os.environ['BUCKET_NAME']

def lambda_handler(event, context):
    # ✅ Handle OPTIONS preflight request
    if event['httpMethod'] == 'OPTIONS':
        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "*",
                "Access-Control-Allow-Methods": "POST,OPTIONS"
            },
            "body": json.dumps("OK")
        }

    try:
        # ✅ Parse body
        body = json.loads(event['body'])
        image_data = base64.b64decode(body['file'])
        filename = body['filename']

        # ✅ Validate extension
        ext = filename.split('.')[-1].lower()
        if ext not in ALLOWED_EXTENSIONS:
            return {
                "statusCode": 400,
                "headers": {
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Headers": "*"
                },
                "body": json.dumps({"error": "Invalid file type. Only jpg, jpeg, png allowed."})
            }

        # ✅ Upload to S3
        s3.put_object(
            Bucket=BUCKET_NAME,
            Key=filename,
            Body=image_data,
            ContentType=f"image/{ext}"
        )

        # ✅ Success
        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "*"
            },
            "body": json.dumps({"message": "Upload successful"})
        }

    except Exception as e:
        print("Error:", str(e))
        return {
            "statusCode": 500,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "*"
            },
            "body": json.dumps({"error": "Internal server error", "details": str(e)})
        }
