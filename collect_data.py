import os
import requests
import pandas as pd
from dotenv import load_dotenv

# .env Datei laden
load_dotenv()

# Zugriff auf die Secrets
access_token = os.getenv('ACCESS_TOKEN')
user_id = os.getenv('USER_ID')
url = os.getenv('API_URL')

# Daten von der Instagram API abrufen
response = requests.get(f'{url}/{user_id}/media?fields=id,caption,media_type,media_url,permalink,thumbnail_url,timestamp,username,like_count,comments_count&access_token={access_token}')
data = response.json()

# Daten in eine CSV-Datei speichern
df = pd.DataFrame(data['data'])
df.to_csv('instagram_data.csv', index=False)

# Daten analysieren
df['timestamp'] = pd.to_datetime(df['timestamp'])
df['year_month'] = df['timestamp'].dt.to_period('M')
posts_per_month = df.groupby('year_month').size()

# Ergebnisse speichern
posts_per_month.to_csv('posts_per_month.csv')
