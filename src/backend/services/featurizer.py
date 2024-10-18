import librosa
import numpy as np

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