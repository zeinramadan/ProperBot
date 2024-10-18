import os
import pickle
from services.featurizer import extract_features
from services.track_downloader import download_track

# Load the trained model
with open('src/backend/resources/model.pkl', 'rb') as f:
    model = pickle.load(f)

def predict(url):
    try:
        # Step 1: Download the audio from the YouTube link
        audio_path = download_track(url)

        # Step 2: Extract features
        features = extract_features(audio_path)

        # Step 3: Predict using the trained model
        score = model.predict([features])[0]

        # Cleanup downloaded audio
        os.remove(audio_path)

        # Step 4: Return the prediction score
        return float(score)

    except Exception as e:
        raise RuntimeError(f"Prediction failed: {str(e)}")
