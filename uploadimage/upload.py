import json
import boto3
import os
import base64
from datetime import datetime
from urllib.parse import unquote_plus

s3 = boto3.client('s3')
BUCKET_NAME = os.environ.get('BUCKET_NAME')

def lambda_handler(event, context):
    try:
        # Decode the image file from the multipart form-data
        content_type = event['headers'].get('Content-Type') or event['headers'].get('content-type')
        body = base64.b64decode(event['body']) if event.get('isBase64Encoded') else event['body']
        
        # Extract boundary from content-type
        boundary = content_type.split("boundary=")[-1]
        parts = body.split(boundary.encode())

        # Extract image bytes and filename
        for part in parts:
            if b'Content-Disposition' in part and b'filename=' in part:
                header, file_data = part.split(b'\r\n\r\n', 1)
                file_data = file_data.rsplit(b'\r\n', 1)[0]
                disposition = header.decode()
                filename = disposition.split('filename="')[1].split('"')[0]
                
                # Clean filename and add timestamp
                clean_filename = unquote_plus(filename.replace(' ', '_'))
                key = f"uploads/{datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')}_{clean_filename}"

                # Upload to S3
                s3.put_object(Bucket=BUCKET_NAME, Key=key, Body=file_data)
                
                return {
                    "statusCode": 200,
                    "body": json.dumps(f"Image uploaded to {key}")
                }

        return {
            "statusCode": 400,
            "body": "No valid file part found in the request."
        }

    except Exception as e:
        print("Error:", e)
        return {
            "statusCode": 500,
            "body": json.dumps(f"Error uploading image: {str(e)}")
        }
