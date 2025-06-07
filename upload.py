import json
import boto3
import base64
import os
import uuid

s3 = boto3.client('s3')
BUCKET_NAME = os.environ['BUCKET_NAME']

def lambda_handler(event, context):
    try:
        body = json.loads(event['body'])
        image_data = body['image']  # base64 string, like "data:image/png;base64,...."
        image_name = body.get('filename', f"{uuid.uuid4()}.png")
        
        # Extract base64 content after comma
        if ',' in image_data:
            image_data = image_data.split(",")[1]
        
        decoded = base64.b64decode(image_data)
        
        # Upload to S3
        s3.put_object(
            Bucket=BUCKET_NAME,
            Key=image_name,
            Body=decoded,
            ContentType='image/png' if image_name.lower().endswith('.png') else 'image/jpeg'
        )
        
        return {
            "statusCode": 200,
            "body": json.dumps({"message": "Image uploaded successfully", "filename": image_name})
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
