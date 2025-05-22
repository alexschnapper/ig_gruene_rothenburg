import requests
import pandas as pd
import os
from dotenv import load_dotenv
import re

# .env Datei laden
load_dotenv()

ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
USER_ID = os.getenv('USER_ID')


def fetch_instagram_data():
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
    posts_df.to_csv('data/instagram_data.csv', index=False)

    # Follower-Daten anhängen, wenn die Datei bereits existiert
    if os.path.exists('data/instagram_followers.csv'):
        existing_followers_df = pd.read_csv('data/instagram_followers.csv')
        existing_followers_df['timestamp'] = pd.to_datetime(existing_followers_df['timestamp'])
        followers_df = pd.concat([existing_followers_df, followers_df], ignore_index=True)

    followers_df.to_csv('data/instagram_followers.csv', index=False)
    
    # Interaktionen pro Account berechnen
    posts_df['interactions'] = posts_df['like_count'] + posts_df['comments_count']
    interactions_per_account = posts_df.groupby('username')['interactions'].sum().reset_index()

    # Speichern der aufbereiteten Daten
    interactions_per_account.to_csv('data/interactions_per_account.csv', index=False)

    # Verweise (Mentions) extrahieren
    mentions = []
    for index, row in posts_df.iterrows():
        if pd.notnull(row['caption']):
            found_mentions = re.findall(r'@(\w+)', row['caption'])
            for mention in found_mentions:
                mentions.append({'mentioned_account': mention, 'post_id': row['id']})

    mentions_df = pd.DataFrame(mentions)
    mentions_count = mentions_df['mentioned_account'].value_counts().reset_index()
    mentions_count.columns = ['mentioned_account', 'count']

    # Speichern der Verweise (Mentions)
    mentions_count.to_csv('data/mentions_count.csv', index=False)

if __name__ == "__main__":
    fetch_instagram_data()
