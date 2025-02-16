import os
import requests
import pandas as pd
from dotenv import load_dotenv

# .env Datei laden
load_dotenv()

# Zugriff auf die Secrets
access_token = os.getenv('ACCESS_TOKEN')
user_id = os.getenv('USER_ID')
url = f"https://graph.instagram.com"

def fetch_instagram_data():
    # Daten von der Instagram API abrufen
    response = requests.get(f'{url}/{user_id}/media?fields=id,caption,media_type,media_url,permalink,thumbnail_url,timestamp,username,like_count,followers_count,comments_count&access_token={access_token}')
    data = response.json()

    # Daten in eine CSV-Datei speichern
    df = pd.DataFrame(data['data'])
    df.to_csv('instagram_data.csv', index=False)

    # Daten analysieren für Posts pro Monat
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['year_month'] = df['timestamp'].dt.to_period('M')
    posts_per_month = df.groupby('year_month').size()

    # Ergebnisse speichern
    posts_per_month.to_csv('posts_per_month.csv')


def fetch_instagram_followers():
    # Abrufen der Medien-Daten
    media_url = f"https://graph.instagram.com/{USER_ID}/media?fields=id,caption,media_type,media_url,permalink,thumbnail_url,timestamp,username,like_count,comments_count&access_token={ACCESS_TOKEN}"
    media_response = requests.get(media_url)
    media_data = media_response.json()

    posts = media_data['data']
    posts_df = pd.DataFrame(posts)
    posts_df['timestamp'] = pd.to_datetime(posts_df['timestamp'])

    # Abrufen der Follower-Daten
    user_url = f"https://graph.instagram.com/{USER_ID}?fields=followers_count&access_token={ACCESS_TOKEN}"
    user_response = requests.get(user_url)
    user_data = user_response.json()

    followers_count = user_data['followers_count']
    followers_df = pd.DataFrame([{'timestamp': pd.Timestamp.now(), 'followers_count': followers_count}])

    # Speichern der Daten
    posts_df.to_csv('instagram_data.csv', index=False)

    # Follower-Daten anhängen, wenn die Datei bereits existiert
    if os.path.exists('instagram_followers.csv'):
        existing_followers_df = pd.read_csv('instagram_followers.csv')
        existing_followers_df['timestamp'] = pd.to_datetime(existing_followers_df['timestamp'])
        followers_df = pd.concat([existing_followers_df, followers_df], ignore_index=True)

    followers_df.to_csv('instagram_followers.csv', index=False)

if __name__ == "__main__":
    fetch_instagram_data()
