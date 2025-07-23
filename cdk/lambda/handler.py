import boto3
import os

def main(event, context):
    s3 = boto3.client('s3')
    bucket = "cdk-hnb659fds-assets-905418307092-eu-west-2"
    response = s3.list_objects_v2(Bucket=bucket)
    files = [obj['Key'] for obj in response.get('Contents', [])]
    print(files)
    return files

if __name__ == "__main__":
    # For local testing, you can call the main function directly
    print(main({}, {}))