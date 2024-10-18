import unittest
from fastapi.testclient import TestClient
from src.backend.main import app
from src.backend.models.YoutubeLink import YouTubeLink

class TestPredictEndpoint(unittest.TestCase):

    def setUp(self):

        self.client = TestClient(app)

    def test_predict_success(self):

        # Assuming a valid YouTube URL for testing
        youtube_link = YouTubeLink(url="https://www.youtube.com/watch?v=dQw4w9WgXcQ")
        response = self.client.post("/predict/", json=youtube_link.model_dump())
        
        # Check if the response status code is 200
        self.assertEqual(response.status_code, 200)
        
        # Check if the response contains a score
        self.assertIn("score", response.json())

    def test_predict_invalid_url(self):
        # Assuming an invalid YouTube URL for testing
        youtube_link = YouTubeLink(url="invalid_url")
        response = self.client.post("/predict/", json=youtube_link.model_dump())    
        
        # Check if the response status code is 500
        self.assertEqual(response.status_code, 500)
        
        # Check if the response contains an error detail
        self.assertIn("detail", response.json())

if __name__ == "__main__":
    unittest.main()

