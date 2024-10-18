import unittest
import numpy as np
from src.backend.services.featurizer import extract_features

class TestFeaturizer(unittest.TestCase):

    def test_extract_features(self):
        # Assuming you have a sample audio file for testing
        test_audio_path = 'test_audio.wav'
        features = extract_features(test_audio_path)
        
        # Check if the features are a numpy array
        self.assertIsInstance(features, np.ndarray)
        
        # Check if the features have the expected length
        expected_length = 13 + 12 + 7 + 1 + 1 + 1  # Adjust based on your feature extraction
        self.assertEqual(len(features), expected_length)

if __name__ == '__main__':
    unittest.main()