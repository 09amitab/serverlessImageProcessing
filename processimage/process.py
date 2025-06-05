import boto3
import os
from PIL import Image, ImageOps
import tempfile

s3 = boto3.client('s3')

def lambda_handler(event, context):
    try:
        for record in event['Records']:
            bucket = record['s3']['bucket']['name']
            key = record['s3']['object']['key']

            print(f"Processing image: s3://{bucket}/{key}")

            # Download image
            with tempfile.TemporaryDirectory() as tmpdir:
                tmp_path = os.path.join(tmpdir, os.path.basename(key))
                s3.download_file(bucket, key, tmp_path)

                # Open and process image
                image = Image.open(tmp_path)
                processed_image = ImageOps.grayscale(image)  # You can change this to sketch, etc.

                # Save processed image
                processed_key = f"processed/{key}"
                processed_path = os.path.join(tmpdir, f"processed-{os.path.basename(key)}")
                processed_image.save(processed_path)

                # Upload back to S3
                s3.upload_file(processed_path, bucket, processed_key)

        return {"statusCode": 200, "body": "Processing complete"}

    except Exception as e:
        print("Error processing image:", str(e))
        return {"statusCode": 500, "body": str(e)}
