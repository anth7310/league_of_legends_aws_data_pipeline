import json
import requests
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
    """ Get the summoner json and upload into S3.
    Label as puuid
    """
    lol_watcher     = LolWatcher(API_KEY, default_status_v4=True)
    region          = event['region']
    summoner_name   = event['summoner_name']
    summoner = lol_watcher.summoner.by_name(region, summoner_name)

    s3_client = boto3.client(
        's3',
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY,
    )
    
    uploadByteStream = bytes(json.dumps(summoner).encode('UTF-8'))

    folder = f'raw_summoner_dto'
    file_name = f"{folder}/{summoner['puuid']}.json"

    s3_put_response = s3_client.put_object(Bucket=BUCKET, Key=file_name, Body=uploadByteStream)

    return {
        'riot_api_response': summoner,
        's3_put_response': s3_put_response
    }


if __name__ == "__main__":
    log_folder_name = f'./logs/{time.time()}'
    os.makedirs(log_folder_name, exist_ok=True)
    event = {
        'region': 'NA1',
        'summoner_name': 'amacss',
    }
    response = lambda_handler(event)
    puuid = response['riot_api_response']['puuid']
    with open(f'./{log_folder_name}/{event["region"]}-{puuid}.json', 'w') as f:
        f.write(json.dumps(lambda_handler(event)))