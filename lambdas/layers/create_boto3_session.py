import boto3
from botocore.exceptions import ClientError
import os

def create_boto3_session(region_name):
    access_key = os.environ.get('ACCESS_KEY')
    secret_key = os.environ.get('SECRET_KEY')
    
    if access_key and secret_key:
        # Use credentials from environment variables in development
        session = boto3.session.Session(
            region_name = region_name,
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key
        )
    else:
        # Use IAM role credentials in production
        session = boto3.session.Session(
            region_name = region_name
        )
    return session