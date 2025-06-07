import boto3
import os
import json
from PIL import Image, ImageOps
import tempfile

s3 = boto3.client('s3')

def lambda_handler(event, context):
    try:
        for record in event['Records']:
            bucket = record['s3']['bucket']['name']
            key = record['s3']['object']['key']

            print(f"Processing image: s3://{bucket}/{key}")

            # Create temporary working directory
            with tempfile.TemporaryDirectory() as tmpdir:
                # Download image to temp path
                tmp_path = os.path.join(tmpdir, os.path.basename(key))
                s3.download_file(bucket, key, tmp_path)

                # Open and process the image (convert to grayscale)
                image = Image.open(tmp_path)
                processed_image = ImageOps.grayscale(image)

                # Save the processed image
                processed_key = f"processed/{key}"
                processed_path = os.path.join(tmpdir, f"processed-{os.path.basename(key)}")
                processed_image.save(processed_path)

                # Upload processed image back to S3
                s3.upload_file(processed_path, bucket, processed_key)

        # Return success response
        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "*",
                "Access-Control-Allow-Methods": "POST,OPTIONS,GET"
            },
            "body": json.dumps({"message": "Image processed and uploaded successfully"})
        }

    except Exception as e:
        print("Error processing image:", str(e))
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
