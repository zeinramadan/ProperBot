from fastapi import FastAPI, HTTPException
from google.oauth2.credentials import Credentials
from fastapi.middleware.cors import CORSMiddleware
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import re

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Update with your frontend's URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Gmail API settings
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

# Regular expression to find SoundCloud links
SOUNDCLOUD_REGEX = r"(https?://soundcloud\.com/[^\s]+)"

def authenticate_gmail():

    # Use credentials.json file for OAuth2 authentication
    flow = InstalledAppFlow.from_client_secrets_file(
        "credentials.json", SCOPES
    )
    creds = flow.run_local_server(port=56565)
    return creds

def get_soundcloud_links(creds) -> list:
    links = []
    try:
        service = build("gmail", "v1", credentials=creds)

        # List messages in the inbox
        results = service.users().messages().list(userId="me").execute()
        messages = results.get("messages", [])

        for message in messages:
            msg = service.users().messages().get(userId="me", id=message["id"], format="full").execute()
            email_body = msg["snippet"]

            # Find all SoundCloud links in the email snippet
            matches = re.findall(SOUNDCLOUD_REGEX, email_body)
            for match in matches:
                print(f"Found SoundCloud URL: {match}")  # Debugging line
                links.append(match)

    except Exception as e:
        print(f"Error fetching emails: {e}")
    
    return links

import urllib.parse

def generate_private_soundcloud_embed_url(private_playlist_url):
    base_url = "https://w.soundcloud.com/player/"
    # Extract the playlist ID and secret token from the URL
    match = re.search(r"soundcloud\.com/([^/]+)/sets/([^/]+)/s-([a-zA-Z0-9]+)", private_playlist_url)
    if match:
        user, playlist, secret_token = match.groups()
        api_url = f"https://api.soundcloud.com/playlists/{playlist}?secret_token=s-{secret_token}"
    else:
        raise ValueError("Invalid SoundCloud private playlist URL format")

    params = {
        'url': api_url,
        'color': '#ff5500',
        'auto_play': 'false',
        'hide_related': 'false',
        'show_comments': 'true',
        'show_user': 'true',
        'show_reposts': 'false',
        'show_teaser': 'true'
    }
    query_string = urllib.parse.urlencode(params)
    embed_url = f"{base_url}?{query_string}"
    return embed_url

# # Example usage
# private_playlist_url = "https://soundcloud.com/your-username/your-playlist-name/s-abcdefg"
# embed_url = generate_private_soundcloud_embed_url(private_playlist_url)
# print(embed_url)

@app.get("/soundcloud-links")
async def soundcloud_links():
    creds = authenticate_gmail()
    links = get_soundcloud_links(creds)
    if not links:
        raise HTTPException(status_code=404, detail="No SoundCloud links found")
    
    embed_urls = []
    for link in links:
        try:
            embed_url = generate_private_soundcloud_embed_url(link)
            embed_urls.append(embed_url)
        except Exception as e:
            print(f"Error generating embed URL for {link}: {e}")  # Debugging line
    
    return embed_urls
