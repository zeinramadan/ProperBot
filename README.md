# ProperBot

This project is for creating a Reddit bot that uses a ML model to automatically assign a score to each track posted in the r/ProperTechno subreddit. The score describes how likely the track fits the vibe of proper techno.
## Ressources

### Machine Learning Model + feature extraction
1. https://www.section.io/engineering-education/machine-learning-for-audio-classification/

### Building the Reddit Bot 
1. Understand the Reddit API: https://new.pythonforengineers.com/blog/build-a-reddit-bot-part-1/
2. Using the API and making the bot: https://new.pythonforengineers.com/blog/build-a-reddit-bot-part-2-reply-to-posts/
3. Automating the bot: https://new.pythonforengineers.com/blog/build-a-reddit-bot-part-3-automate-your-bot/
4. Downloading youtube videos as mp3 with python: https://www.geeksforgeeks.org/download-video-in-mp3-format-using-pytube/
5. For bandcamp, we need to automate the way Mike (flashback jack) does it: Go the bandcamp page for the track, inspect element, network section, click play on the bandcamp page, fetch the url request made to listen to the track (starts with https://t4.bcbits.com/), then save the audio file. We will get 128k mp3 files.

### Dataset

1. Positive cases: Proper Techno spotify playlist -> https://open.spotify.com/playlist/0E6pf5W3NV7armcJYfNK3H?si=826f2122a6b843c8
2. Negative cases: 
    1. DARK /HARD TECHNO: https://open.spotify.com/playlist/1jjzhb9ublCl3X6ZZ6X9kK?si=3ea2988e0b1443e8
    2. ?
