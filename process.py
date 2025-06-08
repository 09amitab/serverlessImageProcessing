import boto3
import os

s3 = boto3.client('s3')
bucket_name = os.environ['BUCKET_NAME']

def lambda_handler(event, context):
    try:
        for record in event['Records']:
            key = record['s3']['object']['key']
            print(f"Processing image: {key}")

            # You can add image manipulation logic here (e.g., resize, convert)

            # Example: just copying it to another prefix
            copy_source = {'Bucket': bucket_name, 'Key': key}
            target_key = f"processed/{key}"
            s3.copy_object(
                Bucket=bucket_name,
                CopySource=copy_source,
                Key=target_key
            )
        return {'statusCode': 200, 'body': 'Image processed'}
    except Exception as e:
        print(f"Error processing image: {str(e)}")
        return {'statusCode': 500, 'body': str(e)}
