import os
import pickle
from services.featurizer import extract_features
from services.track_downloader import download_track
from datetime import datetime
from services.database import initialize_db, insert_track, get_track_by_fingerprint, djv
from dejavu.recognize import FileRecognizer

# Load the trained model
with open('src/backend/resources/model.pkl', 'rb') as f:
    model = pickle.load(f)

# Initialize the database
initialize_db()

def predict(url):
    try:
        # Download the audio from the YouTube link
        audio_path = download_track(url)

        # Fingerprint the audio
        djv.fingerprint_file(audio_path)
        fingerprint = djv.recognize(FileRecognizer, audio_path)

        # Check if the track is already in the database using the fingerprint
        cached_data = get_track_by_fingerprint(fingerprint)
        if cached_data:
            print("Track already in database, using cached data")

            # Get score from cached data to return to user
            _, score = cached_data

        else:
            print("Track not in database, scoring...")

            # Extract features
            features = extract_features(audio_path)

            # Score using the trained model
            score = model.predict([features])[0]

            # Save features, fingerprint, and score to the database
            insert_track(url, features, fingerprint, score, datetime.now().isoformat())

        # Cleanup downloaded audio
        os.remove(audio_path)

        # Return the prediction score
        return float(score)

    except Exception as e:
        raise RuntimeError(f"Prediction failed: {str(e)}")
