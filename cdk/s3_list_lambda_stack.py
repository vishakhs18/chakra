from aws_cdk import (
    aws_lambda as _lambda,
    aws_iam as iam,
    aws_s3 as s3,
    Stack,
    App
)
from constructs import Construct

class S3ListLambdaStack(Stack):
    def __init__(self, scope: Construct, id: str, bucket_name: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Reference the existing S3 bucket
        bucket = s3.Bucket.from_bucket_name(self, id, bucket_name)

        # Python Lambda function
        lambda_fn = _lambda.Function(
            self, "S3ListLambda",
            runtime=_lambda.Runtime.PYTHON_3_9,
            handler="handler.main",
            code=_lambda.Code.from_asset("lambda"),
            environment={
                'BUCKET_NAME': bucket.bucket_name
            }
        )
        bucket.grant_read(lambda_fn)

        # Rust Lambda function
        rust_lambda_fn = _lambda.Function(
            self, "S3ListRustLambda",
            runtime=_lambda.Runtime.PROVIDED_AL2,
            handler="bootstrap",
            code=_lambda.Code.from_asset("lambda_rust"),
            environment={
                'BUCKET_NAME': bucket.bucket_name
            }
        )
        bucket.grant_read(rust_lambda_fn)

if __name__ == "__main__":
    app = App()
    S3ListLambdaStack(app, "S3ListLambdaStack", bucket_name="cdk-hnb659fds-assets-905418307092-eu-west-2")
    app.synth()
