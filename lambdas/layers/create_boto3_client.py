import boto3
from botocore.exceptions import ClientError
import os

def create_boto3_client(service_name, region_name):
    access_key = os.environ.get('ACCESS_KEY')
    secret_key = os.environ.get('SECRET_KEY')

    if access_key and secret_key:
        # Use credentials from environment variables in development
        client = boto3.client(
            service_name,
            region_name = region_name,
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key
        )
    else:
        # Use IAM role credentials in production
        client = boto3.client(
            service_name, 
            region_name=region_name
        )
    return client