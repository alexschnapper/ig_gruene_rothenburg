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
response = requests.get(f'{url}/{user_id}/media?fields=id,caption,media_type,media_url,thumbnail_url,timestamp,username,insights.metric(impressions,reach,engagement)&access_token={access_token}')
data = response.json()

# Ausgabe der API-Antwort zur Überprüfung
print(data)

# Überprüfen, ob die API-Antwort den Schlüssel 'data' enthält
if 'data' not in data:
    raise KeyError("Die API-Antwort enthält keinen 'data'-Schlüssel. Antwort: {}".format(data))

# Daten in eine CSV-Datei speichern
df = pd.DataFrame(data['data'])
os.makedirs('data', exist_ok=True)  # Verzeichnis erstellen, falls es nicht existiert
df.to_csv('data/instagram_data.csv', index=False)

# Daten analysieren
df['timestamp'] = pd.to_datetime(df['timestamp'])
df['year_month'] = df['timestamp'].dt.to_period('M')

# Anzahl der Beiträge pro Monat
posts_per_month = df.groupby('year_month').size()

# Engagement, Impressions und Reach pro Monat
df['impressions'] = df['insights'].apply(lambda x: x['impressions']['value'] if 'impressions' in x else 0)
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