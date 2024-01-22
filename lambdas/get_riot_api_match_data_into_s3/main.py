import json
import requests
import os
from riotwatcher import LolWatcher, ApiError


API_KEY = os.environ.get('RIOT_GAMES_API_KEY')

def lambda_handler(event=None, context=None):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
        "Origin": "https://developer.riotgames.com",
        "X-Riot-Token": API_KEY
    }

    # get summoner puuid
    name = "amacss"
    url = f'https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{name}'
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return {
            'statusCode': response.status_code,
            'body': response.json()
        }
    
    puuid = response.json()['puuid']

    # get latest match history ids
    count = 100
    url = f"https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?start=0&count={count}"
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return {
            'statusCode': response.status_code,
            'body': response.json()
        }
    
    match_id_history = response.json()
    match_id = match_id_history[0]
    
    # get match information
    url = f"https://americas.api.riotgames.com/lol/match/v5/matches/{match_id}"
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return {
            'statusCode': response.status_code,
            'body': response.json()
        }


    # download data from riot api
    # store into s3 bucket
    return {
        'statusCode': 200,
        'body': response.json()
    }

if __name__ == "__main__":
    body = lambda_handler()['body']
    match_id = body['metadata']['matchId']
    with open(f'{match_id}.json', 'w') as f:
        f.write(json.dumps(body))