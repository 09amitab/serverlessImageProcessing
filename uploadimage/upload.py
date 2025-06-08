import boto3
import os
import uuid

s3 = boto3.client('s3')
bucket_name = os.environ['BUCKET_NAME']

def lambda_handler(event, context):
    try:
        content_type = event['headers'].get('Content-Type') or event['headers'].get('content-type')
        if content_type and content_type.startswith('multipart/form-data'):
            return {
                'statusCode': 400,
                'body': 'Use a base64-encoded image in request body instead of multipart/form-data.'
            }

        image_data = event['body']
        is_base64_encoded = event.get("isBase64Encoded", False)
        if is_base64_encoded:
            import base64
            image_data = base64.b64decode(image_data)
        else:
            image_data = image_data.encode('utf-8')

        # Generate unique filename
        filename = f"{uuid.uuid4()}.jpg"

        s3.put_object(
            Bucket=bucket_name,
            Key=filename,
            Body=image_data,
            ContentType='image/jpeg'
        )

        return {
            'statusCode': 200,
            'body': f"Image uploaded as {filename}"
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': f"Error: {str(e)}"
        }
