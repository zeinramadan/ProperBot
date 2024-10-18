import unittest
from unittest.mock import patch
from src.backend.services.predictor import predict

class TestPredictor(unittest.TestCase):

    @patch('src.backend.services.predictor.download_track')
    @patch('src.backend.services.predictor.extract_features')
    @patch('src.backend.services.predictor.model')
    def test_predict(self, mock_model, mock_extract_features, mock_download_track):
        
        # Mock the download_track function to return a fake path
        mock_download_track.return_value = 'fake_path.wav'
        
        # Mock the extract_features function to return a fake feature array
        mock_extract_features.return_value = [0.1] * 35  # Adjust based on your feature length
        
        # Mock the model's predict method
        mock_model.predict.return_value = [0.9]
        
        # Call the predict function
        score = predict('https://www.youtube.com/watch?v=example')
        
        # Check if the score is as expected
        self.assertEqual(score, 0.9)

if __name__ == '__main__':
    unittest.main()