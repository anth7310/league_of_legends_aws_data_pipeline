# Use this code snippet in your app.
# If you need more information about configurations
# or implementing the sample code, visit the AWS docs:
# https://aws.amazon.com/developer/language/python/

from botocore.exceptions import ClientError
from create_boto3_session import create_boto3_session
import json

def get_secret():

    secret_name = "riot-games-api"
    service_name='secretsmanager'
    region_name = "us-east-2"

    # Create a Secrets Manager client
    session = create_boto3_session(region_name)
    client = session.client(
        service_name='secretsmanager'
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        # For a list of exceptions thrown, see
        # https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
        raise e
    secret = json.loads(get_secret_value_response['SecretString'])
    return secret

    # Your code goes here.
if __name__ == "__main__":
    print(get_secret())
