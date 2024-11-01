from fastapi import FastAPI, HTTPException
from google.oauth2.credentials import Credentials
from fastapi.middleware.cors import CORSMiddleware
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import re
import requests

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
                print(f"Found SoundCloud URL: {match}")
                links.append(match)

    except Exception as e:
        print(f"Error fetching emails: {e}")
    
    return links

def get_oembed_html(track_url: str) -> str:
    """Fetches oEmbed HTML embed code for a SoundCloud track or playlist URL."""
    try:
        response = requests.get(
            "https://soundcloud.com/oembed",
            params={"format": "json", "url": track_url}
        )
        
        if response.status_code != 200:
            raise ValueError("Failed to fetch oEmbed data from SoundCloud")

        data = response.json()
        return data["html"]  # Contains the full HTML embed code
    except Exception as e:
        print(f"Error fetching oEmbed data: {e}")
        raise HTTPException(status_code=400, detail="Invalid SoundCloud URL")

@app.get("/soundcloud-embed-codes")
async def soundcloud_embed_codes():
    creds = authenticate_gmail()
    links = get_soundcloud_links(creds)
    if not links:
        raise HTTPException(status_code=404, detail="No SoundCloud links found")
    
    embed_codes = []
    for link in links:
        try:
            embed_html = get_oembed_html(link)
            embed_codes.append(embed_html)
        except Exception as e:
            print(f"Error generating embed code for {link}: {e}")

    return {"embed_codes": embed_codes}
