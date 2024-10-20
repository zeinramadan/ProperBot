import os
import pickle
from datetime import datetime
import librosa
import numpy as np

from services.track_downloader import download_track
from services.database import initialize_db, insert_track


# Load the trained model
with open('src/backend/resources/model.pkl', 'rb') as f:
    model = pickle.load(f)

# Initialize the database
initialize_db()


# Function to extract features from the audio
def extract_features(file_path):
    y, sr = librosa.load(file_path)

    # Extract features
    mfccs = np.mean(librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13).T, axis=0)
    chroma = np.mean(librosa.feature.chroma_stft(y=y, sr=sr).T, axis=0)
    spectral_contrast = np.mean(librosa.feature.spectral_contrast(y=y, sr=sr).T, axis=0)
    zero_crossings = np.mean(librosa.feature.zero_crossing_rate(y))
    spectral_bandwidth = np.mean(librosa.feature.spectral_bandwidth(y=y, sr=sr))
    rms_energy = np.mean(librosa.feature.rms(y=y))

    # Combine all features into a single array
    features = np.hstack([mfccs, chroma, spectral_contrast, zero_crossings, spectral_bandwidth, rms_energy])
    return features


"""
TODO: understand the fingerprinting process using PyDejaVu or alternative fingerprinting library to implement caching by track fingerprint

Caching logic:
- when we get a track url, first we check if it's in the database by youtube URL
- if youtube url is there, we grab the score from the track_cache table and return it
- if we dont get a youtube url match from track_cache, we then check by fingerprint
- if fingerprint is there, we grab the score from the track_cache table and return it
- if we dont get a fingerprint match from track_cache, we download the track, extract features, score using the model, and save to the database

To implement this we need to understand how the PyDejaVu database is structured and how to query it, and how we can link an entry in track_cache 
to an entry in the PyDejaVu database (ie the fingerprint database)
"""
def predict(url):
    try:
        # Download the audio from the YouTube link
        audio_path = download_track(url)

        # Extract features
        features = extract_features(audio_path)

        # Score using the trained model
        score = model.predict([features])[0]

        # Save features, and score to the database
        insert_track(url, features, score, datetime.now().isoformat())

        # Cleanup downloaded audio
        os.remove(audio_path)

        # Return the prediction score
        return float(score)

    except Exception as e:
        raise RuntimeError(f"Prediction failed: {str(e)}")
