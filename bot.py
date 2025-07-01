import requests
import time
import tweepy
import re
import os

        # === Your Twitter API Keys ===
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_SECRET = os.getenv("ACCESS_SECRET")

        # === Connect to Twitter ===
auth = tweepy.OAuth1UserHandler(API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_SECRET)
api = tweepy.API(auth)

        # This is the URL where the National Weather Service (NWS) posts alerts
NWS_URL = "https://api.weather.gov/alerts/active?area=PA"

def get_alerts():
            response = requests.get(NWS_URL)
            if response.status_code == 200:
                data = response.json()
                alerts = data.get("features", [])
                return alerts
            else:
                print("Failed to get alerts")
                return []

def format_alert(alert):
            properties = alert["properties"]
            event = properties["event"]
            headline = properties["headline"]
            description = properties["description"]
            hail = ""

            # Try to find hail size in the description
            if "hail" in description.lower():
                hail_matches = re.findall(r"([0-9.]+)\s?inch(?:es)?\s?(?:diameter)?\s?hail", description, re.IGNORECASE)
                if hail_matches:
                    hail = f" | Hail: {hail_matches[0]}\""

            return f"{event} for {properties['areaDesc']} until {properties['ends']}{hail}"[:280]

        # Run the bot once for now
alerts = get_alerts()

for alert in alerts:
            message = format_alert(alert)
            print("Posting:", message)
            api.update_status(message)
