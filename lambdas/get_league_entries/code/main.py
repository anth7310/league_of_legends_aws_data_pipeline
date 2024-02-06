import json
import os
from datetime import datetime
from riotwatcher import LolWatcher, ApiError
import time
import itertools
from create_boto3_client import create_boto3_client
from get_secret import get_secret



def lambda_handler(event=None, context=None):

    # AWS bucket
    BUCKET = os.environ.get('BUCKET')
    API_KEY = get_secret()['RIOT_GAMES_API_KEY']

    lol_watcher     = LolWatcher(API_KEY, default_status_v4=True)
    region          = event['region']
    queue           = event['queue']
    tier            = event['tier']
    division        = event['division']
    page            = event['page']

    # league entries
    data = lol_watcher.league.entries(region, queue, tier, division, page)

    json_data = {
        'status': 200,
        'body': data
    }

    # upload into s3 bucket - partition by year/month/day
    current_year = datetime.now().year
    current_month = datetime.now().month
    current_day = datetime.now().day

    folder = f'raw_league_entry_dto/year={current_year}/month={current_month}/day={current_day}'
    file_name = f'{folder}/{region}-{division}-{tier}-{queue}-{page}.json'

    
    s3_client = create_boto3_client('s3')
    
    uploadByteStream = bytes(json.dumps(json_data).encode('UTF-8'))

    s3_put_response = s3_client.put_object(Bucket=BUCKET, Key=file_name, Body=uploadByteStream)

    return {
        'riot_api_response': data,
        's3_put_response': s3_put_response
    }


if __name__ == "__main__":
    # log_folder_name = f'./logs/{time.time()}'
    # os.makedirs(log_folder_name, exist_ok=True)
    # regions = ['NA1']
    # queues = ['RANKED_SOLO_5x5']
    # tiers = ['DIAMOND', 'EMERALD', 'PLATINUM', 'GOLD', 'SILVER', 'BRONZE', 'IRON']
    # divisions = ['I', 'II', 'III', 'IV']
    # pages = list(range(1, 11))
    # total_iter = len(regions) * len(queues) * len(tiers) * len(divisions) * len(pages)
    # for curr_iter, (region, queue, tier, division, page) in enumerate(itertools.product(regions, queues, tiers, divisions, pages)):
    #     print(f"Processing iteration {curr_iter+1}/{total_iter}")
    #     # 20 requests per second
    #     if (curr_iter + 1) % 20 == 0:
    #         time.sleep(1)
    #     event = {
    #         'region': region,
    #         'queue': queue,
    #         'tier': tier,
    #         'division': division,
    #         'page': page
    #     }
    #     response = lambda_handler(event)
    #     with open(f'./{log_folder_name}/{region}-{division}-{tier}-{queue}-{page}.json', 'w') as f:
    #         f.write(json.dumps(response))
    
    event = {
        "region": "NA1",
        "queue": "RANKED_SOLO_5x5",
        "tier": "DIAMOND",
        "division": "I",
        "page": 1
    }
    print(lambda_handler(event))