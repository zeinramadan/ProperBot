from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import subprocess
import librosa
import numpy as np
import os
import shutil
from services.featurizer import extract_features
from services.track_downloader import download_track

# Assuming you have your trained model loaded
# For example, using pickle (replace with your actual model loading)
import pickle

with open('model.pkl', 'rb') as f:
    model = pickle.load(f)

app = FastAPI()

class YouTubeLink(BaseModel):
    url: str

# Helper function to download YouTube video and extract audio
def download_audio(youtube_url):
    # Ensure you have yt-dlp installed
    command = [
        'yt-dlp', youtube_url, '-x', '--audio-format', 'wav', 
        '--output', 'downloaded_audio.%(ext)s'
    ]
    subprocess.run(command, check=True)
    return 'downloaded_audio.wav'

# Function to extract features from the audio
def extract_features(file_path):
    y, sr = librosa.load(file_path)

    # Extract features as we discussed earlier
    tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
    mfccs = np.mean(librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13).T, axis=0)
    spectral_contrast = np.mean(librosa.feature.spectral_contrast(y=y, sr=sr).T, axis=0)

    features = np.hstack([tempo, mfccs, spectral_contrast])
    return features

@app.post("/predict/")
async def predict_track(data: YouTubeLink):
    try:
        # Step 1: Download the audio from the YouTube link
        audio_path = download_audio(data.url)

        # Step 2: Extract features
        features = extract_features(audio_path)

        # Step 3: Predict using the trained model
        score = model.predict([features])[0]

        # Cleanup downloaded audio
        os.remove(audio_path)

        # Step 4: Return the prediction score
        return {"score": float(score)}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

