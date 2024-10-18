import unittest
from unittest.mock import patch, MagicMock
from src.backend.services.track_downloader import is_valid_youtube_link, download_track

class TestTrackDownloader(unittest.TestCase):

    def test_is_valid_youtube_link(self):
        valid_url = "https://www.youtube.com/watch?v=example"
        invalid_url = "https://www.notyoutube.com/watch?v=example"
        
        self.assertTrue(is_valid_youtube_link(valid_url))
        self.assertFalse(is_valid_youtube_link(invalid_url))

    @patch('src.backend.services.track_downloader.YouTube')
    def test_download_track(self, mock_youtube):
        # Mock the YouTube object and its methods
        mock_stream = MagicMock()
        mock_streams = MagicMock()
        mock_streams.filter.return_value.first.return_value = mock_stream
        mock_youtube.return_value.streams = mock_streams
        
        # Call the download_track function
        download_track('https://www.youtube.com/watch?v=example')
        
        # Check if the download method was called
        mock_stream.download.assert_called_once()

if __name__ == '__main__':
    unittest.main()