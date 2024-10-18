import re
from pytube import YouTube

def is_valid_youtube_link(url):
    """
    Check if the provided URL is a valid YouTube link.
    """
    youtube_regex = (
        r'(https?://)?(www\.)?'
        '(youtube|youtu|youtube-nocookie)\.(com|be)/'
        '(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})')
    youtube_regex_match = re.match(youtube_regex, url)
    return youtube_regex_match is not None

def download_track(url, output_path='.'):
    """
    Download a track from YouTube using the provided URL.
    """
    if not is_valid_youtube_link(url):
        raise ValueError("Invalid YouTube URL")

    try:
        yt = YouTube(url)
        # Select the first audio stream
        audio_stream = yt.streams.filter(only_audio=True).first()
        if audio_stream:
            audio_stream.download(output_path=output_path)
            print(f"Downloaded: {yt.title}")
        else:
            print("No audio stream available for this video.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage:
# url = "https://www.youtube.com/watch?v=example"
# if is_valid_youtube_link(url):
#     download_youtube_track(url, output_path='/path/to/save')