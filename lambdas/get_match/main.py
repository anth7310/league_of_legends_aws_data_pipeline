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

def get_match_history(region, puuid, count, start_time):
    lol_watcher = LolWatcher(API_KEY, default_status_v4=True)
    match_history = lol_watcher.match.matchlist_by_puuid(region=region, puuid=puuid, count=count, start_time=start_time)
    return match_history

def get_match(region, match_id):
    lol_watcher = LolWatcher(API_KEY, default_status_v4=True)
    match = lol_watcher.match.by_id(region, match_id)
    return match

def lambda_handler(event=None, context=None):
    """ Get match data from riot API and upload into s3 bucket
    """
    region      = event['region']
    puuid       = event['puuid']
    count       = event['count']
    start_time  = event['start_time']

    match_history = get_match_history(region, puuid, count, start_time)
    
    folder = f'raw_match_dto'
    s3_client = boto3.client(
        's3',
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY,
        )
    riot_responses = []
    s3_responses = []
    for match_id in match_history:
        # match data
        data = get_match(region, match_id)
        riot_responses.append(data)
        
        file_name = f'{folder}/{region}-{match_id}.json'

        json_data = {
            'status': 200,
            'riot_api_response': data
        }
        
        uploadByteStream = bytes(json.dumps(json_data).encode('UTF-8'))

        s3_put_response = s3_client.put_object(Bucket=BUCKET, Key=file_name, Body=uploadByteStream)
        s3_responses.append(s3_put_response)

    return {
        'riot_api_response': riot_responses,
        's3_put_response': s3_responses
    }


if __name__ == "__main__":
    # testing
    region = 'NA1'

    # Get the current time in epoch seconds
    current_time = time.time()

    # Number of seconds in 24 hours
    seconds_in_24_hours = 24 * 60 * 60

    # Calculate the epoch time for 24 hours ago
    time_24_hours_ago = int(current_time - seconds_in_24_hours)

    puuid = 'He53uK1xaWDU347Z33yOeZeosmYv4nWT0IGK2XlIVxiJIWSce9JyhNPjsIAwqY1O3oa2vkMWFAW1FA'
    event = {
        'region': region,
        'puuid': puuid,
        'count': 24,
        'start_time': time_24_hours_ago
    }
    log_folder_name = f'./logs/{time.time()}'
    os.makedirs(log_folder_name, exist_ok=True)
    with open(f'./{log_folder_name}/{region}-{puuid}.json', 'w') as f:
        f.write(json.dumps(lambda_handler(event)))