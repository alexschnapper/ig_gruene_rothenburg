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
url2 = f"https://graph.facebook.com"

def fetch_instagram_data():
    # Daten von der Instagram API abrufen
    response = requests.get(f'{url}/{user_id}/media?fields=id,caption,media_type,media_url,permalink,thumbnail_url,timestamp,username,insights.metric(impressions,reach,engagement),like_count,followers_count,comments_count&access_token={access_token}')
    data = response.json()

    # Daten in eine CSV-Datei speichern
    df = pd.DataFrame(data['data'])
    os.makedirs('data', exist_ok=True)  # Verzeichnis erstellen, falls es nicht existiert
    df.to_csv('data/instagram_data.csv', index=False)

    # Daten analysieren für Posts pro Monat
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['year_month'] = df['timestamp'].dt.to_period('M')
    # Anzahl der Beiträge pro Monat
    posts_per_month = df.groupby('year_month').size()
    
    # Engagement, Impressions und Reach pro Monat
    df['impressions'] = df ['insights'].apply(lambda x: x['impressions']['value'] if 'impressions' in x else 0)
    df['reach'] = df['insights'].apply(lambda x: x['reach']['value'] if 'reach' in x else 0)
    df['engagement'] = df['insights'].apply(lambda x: x['engagement']['value'] if 'engagement' in x else 0)

    impressions_per_month = df.groupby('year_month')['impressions'].sum()
    reach_per_month = df.groupby('year_month')['reach'].sum()
    engagement_per_month = df.groupby('year_month')['engagement'].sum()

    # Ergebnisse speichern
    posts_per_month.to_csv('data/posts_per_month.csv')
    impressions_per_month.to_csv('data/impressions_per_month.csv')
    reach_per_month.to_csv('data/reach_per_month.csv')
    engagement_per_month.to_csv('data/engagement_per_month.csv')
    

def fetch_instagram_other():
    # Abrufen der Medien-Daten
    media_url = f"https://graph.instagram.com/{USER_ID}/media?fields=id,caption,media_type,media_url,permalink,thumbnail_url,timestamp,username,like_count,comments_count,account_type,followers_count,follows_count,media_count&access_token={ACCESS_TOKEN}"
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
    os.makedirs('data', exist_ok=True)  # Verzeichnis erstellen, falls es nicht existiert
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
    fetch_instagram_data
    fetch_instagram_other
