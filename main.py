import os
import openai
import requests
from gtts import gTTS
from spotipy.oauth2 import SpotifyOAuth
import spotipy
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API keys and credentials
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
NOTEBOOKLM_API_KEY = os.getenv("NOTEBOOKLM_API_KEY")
SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
SPOTIFY_REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI")

# Authenticate with APIs
openai.api_key = OPENAI_API_KEY

# Spotify authentication
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIFY_CLIENT_ID,
                                               client_secret=SPOTIFY_CLIENT_SECRET,
                                               redirect_uri=SPOTIFY_REDIRECT_URI,
                                               scope="user-library-read user-library-modify"))

def generate_highlights():
    # Fetch cricket match highlights from ChatGPT
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt="Provide a 300-400 word summary of the latest Indian Men's cricket match highlights.",
        max_tokens=350
    )
    return response.choices[0].text.strip()

def upload_to_notebooklm(content):
    url = "https://api.notebooklm.google.com/v1/generate"
    headers = {"Authorization": f"Bearer {NOTEBOOKLM_API_KEY}"}
    data = {
        "content": content,
        "customize": "Podcast length should be only 2 to 3 minutes."
    }
    response = requests.post(url, headers=headers, json=data)
    return response.json().get("generated_text")

def text_to_speech(text):
    tts = gTTS(text, lang="en")
    audio_file = "podcast.mp3"
    tts.save(audio_file)
    return audio_file

def upload_to_spotify(audio_file, title, description):
    # Spotify API to upload podcast
    # Replace this with an appropriate endpoint once Spotify provides one for direct uploads
    print(f"Uploading {audio_file} to Spotify with title '{title}' and description '{description}'")

def main():
    # Step 1: Generate match highlights
    highlights = generate_highlights()

    # Step 2: Customize with NotebookLM
    podcast_script = upload_to_notebooklm(highlights)
    if not podcast_script:
        print("Error generating podcast script")
        return

    # Step 3: Convert script to audio
    audio_file = text_to_speech(podcast_script)

    # Step 4: Upload to Spotify
    upload_to_spotify(audio_file, "Match Highlights Podcast", highlights)

if __name__ == "__main__":
    main()
