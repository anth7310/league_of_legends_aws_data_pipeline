import json
import os
from riotwatcher import LolWatcher, ApiError

import boto3

import time


# AWS bucket
BUCKET = os.environ.get('BUCKET')

API_KEY = os.environ.get('RIOT_GAMES_API_KEY')
ACCESS_KEY = os.environ.get('ACCESS_KEY')
SECRET_KEY = os.environ.get('SECRET_KEY')

def lambda_handler(event=None, context=None):
    """ Get match data from riot API and upload into s3 bucket
    """
    lol_watcher = LolWatcher(API_KEY, default_status_v4=True)
    region      = event['region']
    match_id    = event['match_id']

    # match data
    data = lol_watcher.match.by_id(region, match_id)

    folder = f'raw_match_dto'
    file_name = f'{folder}/{region}-{match_id}.json'

    s3_client = boto3.client(
        's3',
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY,
        )
    
    json_data = {
        'status': 200,
        'riot_api_response': data
    }
    
    uploadByteStream = bytes(json.dumps(json_data).encode('UTF-8'))

    s3_put_response = s3_client.put_object(Bucket=BUCKET, Key=file_name, Body=uploadByteStream)

    return {
        'riot_api_response': data,
        's3_put_response': s3_put_response
    }


if __name__ == "__main__":
    match_id = 'NA1_4901351513'
    region = 'NA1'
    event = {
        'region': region,
        'match_id': match_id
    }
    log_folder_name = f'./logs/{time.time()}'
    os.makedirs(log_folder_name, exist_ok=True)
    with open(f'./{log_folder_name}/{region}-{match_id}.json', 'w') as f:
        f.write(json.dumps(lambda_handler(event)))