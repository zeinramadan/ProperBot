import os
import pickle
from services.featurizer import extract_features
from services.track_downloader import download_track
from datetime import datetime
from services.database import initialize_db, insert_track, get_track

# Load the trained model
with open('src/backend/resources/model.pkl', 'rb') as f:
    model = pickle.load(f)

# Initialize the database
initialize_db()

def predict(url):
    try:
        # Check if the track is already in the database
        cached_features = get_track(url)
        if cached_features:
            # Use cached features
            features = cached_features
        else:
            # Step 1: Download the audio from the YouTube link
            audio_path = download_track(url)

            # Step 2: Extract features
            features = extract_features(audio_path)

            # Save features to the database
            insert_track(url, features, datetime.now().isoformat())

            # Cleanup downloaded audio
            os.remove(audio_path)

        # Step 3: Predict using the trained model
        score = model.predict([features])[0]

        # Step 4: Return the prediction score
        return float(score)

    except Exception as e:
        raise RuntimeError(f"Prediction failed: {str(e)}")
