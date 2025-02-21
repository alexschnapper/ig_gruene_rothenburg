import requests
import csv
import datetime
import os

from dotenv import load_dotenv

# .env Datei laden
load_dotenv()

ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
INSTAGRAM_ID = os.getenv('USER_ID')


def get_follower_count(access_token, instagram_id):
    url = f'https://graph.instagram.com/v12.0/{instagram_id}?fields=id,username,followers_count&access_token={access_token}'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data['followers_count']
    else:
        print(f'Fehler beim Abrufen der Daten: {response.status_code}')
        return None

if __name__ == '__main__':
    follower_count = get_follower_count(ACCESS_TOKEN, INSTAGRAM_ID)
    if follower_count is not None:
        timestamp = datetime.datetime.now().isoformat()
        with open('data/instagram_followers_count.csv', 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([timestamp, follower_count])
        print(f'Follower-Anzahl ({follower_count}) wurde in der CSV-Datei gespeichert.')