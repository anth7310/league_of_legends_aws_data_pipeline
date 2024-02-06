import boto3
from botocore.exceptions import ClientError
import os

def create_boto3_client(service_name):
    region_name = os.environ.get('AWS_REGION')
    access_key = os.environ.get('AWS_ACCESS_KEY_ID')
    secret_key = os.environ.get('AWS_SECRET_ACCESS_KEY')
    session_token = os.environ.get('AWS_SESSION_TOKEN')

    if access_key and secret_key:
        # Use credentials from environment variables in development
        client = boto3.client(
            service_name,
            region_name = region_name,
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            aws_session_token=session_token
        )
    else:
        # Use IAM role credentials in production
        client = boto3.client(
            service_name, 
            region_name=region_name
        )
    return client