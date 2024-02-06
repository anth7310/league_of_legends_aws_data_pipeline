import boto3
from botocore.exceptions import ClientError
import os

def create_boto3_session():
    region_name = os.environ.get('AWS_REGION')
    access_key = os.environ.get('AWS_ACCESS_KEY_ID')
    secret_key = os.environ.get('AWS_SECRET_ACCESS_KEY')
    
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

if __name__ == "__main__":
    session = create_boto3_session()
    client = session.client(service_name="secretsmanager")
    secret_name='riot-games-api'
    get_secret_value_response = client.get_secret_value(SecretId=secret_name)
    print(get_secret_value_response)