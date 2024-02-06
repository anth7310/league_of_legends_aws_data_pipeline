# Use this code snippet in your app.
# If you need more information about configurations
# or implementing the sample code, visit the AWS docs:
# https://aws.amazon.com/developer/language/python/

from botocore.exceptions import ClientError
import os
from create_boto3_client import create_boto3_client
import json

def get_secret():
    API_KEY = os.environ.get('RIOT_GAMES_API_KEY')
    if API_KEY:
        return {
            'RIOT_GAMES_API_KEY': API_KEY
        }


    secret_name = "riot-games-api"
    service_name='secretsmanager'

    # Create a Secrets Manager client
    client = create_boto3_client(service_name)

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
