from aws_cdk import (
    aws_lambda as _lambda,
    aws_iam as iam,
    aws_s3 as s3,
    core
)

class S3ListLambdaStack(core.Stack):
    def __init__(self, scope: core.Construct, id: str, bucket_name: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Reference the existing S3 bucket
        bucket = s3.Bucket.from_bucket_name(self, "MyBucket", bucket_name)

        # Lambda function code
        lambda_fn = _lambda.Function(
            self, "S3ListLambda",
            runtime=_lambda.Runtime.PYTHON_3_11,
            handler="handler.main",
            code=_lambda.Code.from_inline(
                """
import boto3
import os

def main(event, context):
    s3 = boto3.client('s3')
    bucket = os.environ['BUCKET_NAME']
    response = s3.list_objects_v2(Bucket=bucket)
    files = [obj['Key'] for obj in response.get('Contents', [])]
    print(files)
    return files
                """
            ),
            environment={
                'BUCKET_NAME': bucket.bucket_name
            }
        )

        # Grant the Lambda function read access to the bucket
        bucket.grant_read(lambda_fn)
