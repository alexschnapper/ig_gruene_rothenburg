import requests
import csv
import datetime
import os
from dotenv import load_dotenv

# .env Datei laden
load_dotenv()

access_token = os.getenv('ACCESS_TOKEN')
instagram_id = os.getenv('USER_ID')
url = os.getenv('API_URL')
apiv = os.getenv('API_VERSION')

# files
ig_followers_count = 'data/instagram_followers_count.csv'

def get_follower_count(url, apiv, access_token, instagram_id):
    url = f'{url}/{apiv}/{instagram_id}?fields=id,username,followers_count&access_token={access_token}'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        print(data)
        return data['followers_count']
    else:
        print(f'Fehler beim Abrufen der Daten: {response.status_code}')
        print(data)
        return None

def get_ig_data(url, apiv, access_token, instagram_id):
    url = f'{url}/{apiv}/{instagram_id}?fields=id,username,followers_count&access_token={access_token}'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data['followers_count']
    else:
        print(f'Fehler beim Abrufen der Daten: {response.status_code}')
        return None

if __name__ == '__main__':
    followers_count = get_follower_count(url, apiv, access_token, instagram_id)
    if followers_count is not None:
        timestamp = datetime.datetime.now().isoformat()
        with open(ig_followers_count, 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([timestamp, followers_count])
        print(f'Follower-Anzahl ({followers_count}) wurde in der CSV-Datei  ({ig_followers_count}) gespeichert.')