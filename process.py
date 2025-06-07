import boto3
import os
from PIL import Image
import io

s3 = boto3.client('s3')
BUCKET_NAME = os.environ.get('BUCKET_NAME')

def lambda_handler(event, context):
    try:
        # Process each record (can be multiple if batch)
        for record in event['Records']:
            key = record['s3']['object']['key']
            bucket = record['s3']['bucket']['name']

            # Download the image
            response = s3.get_object(Bucket=bucket, Key=key)
            img_data = response['Body'].read()

            # Process the image (convert to grayscale as an example)
            image = Image.open(io.BytesIO(img_data))
            gray_image = image.convert('L')  # Convert to grayscale

            # Save processed image to memory
            buffer = io.BytesIO()
            gray_image.save(buffer, format=image.format)
            buffer.seek(0)

            # Define destination key
            dest_key = key.replace("uploads/", "processed/")

            # Upload processed image
            s3.put_object(Bucket=bucket, Key=dest_key, Body=buffer)

            print(f"Processed and uploaded image to {dest_key}")

        return {
            "statusCode": 200,
            "body": "Image processed successfully."
        }

    except Exception as e:
        print("Error processing image:", e)
        return {
            "statusCode": 500,
            "body": f"Error processing image: {str(e)}"
        }
