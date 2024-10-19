# ProperBot

## Introduction

Hello! If you are reading this then you probably came here through my CV, or you just have a weird fascination for my personal projects and spend a lot of time stalking people's github on the internet (get a life sheesh..). As much as I would love to say it, I can't honestly sit here and say, with a straight face that the only reason I built this app was to help out the music scene, which I love dearly (even though there's a lot of phony, shallow, full of themselves idiots in it who are only in it for the wrong reasons). I could also say that the only reason I built this is to help me and my friends moderate the r/ProperTechno subreddit, because we have to sift through 100s of tracks that people post on a daily basis that is absolute commercial TikTok techno garbage which belongs on that swampfest of a subreddit r/Techno, but that's not entirely true either. 
The main reason I built this is because I like being employed and I know companies like candidates who build shit, so I wanted to show you guys that I indeed, can build shit. But only if it's for something I trulu care about (or something that my employer who pays me to build shit wants me to build, totally onboard with that too).

So strap in, and enjoy the most entertaining README you've read all year. If you're a recruiter, and you're reading this, I hope this should be more than enough to convince you that I know how to code. No need to make me reverse a string or implement a linked list in a live coding interview for god's sake. If you came here from the subredddit, don't ever say we don't try to make the sub a better place. I've spent hours on this. It's still shit, but it's something. Anyways, enough (poorly written and unnecessarily vulgar) comedy. Let's actually get into the meat and potatoes.

## Application Overview

The application is a simple website that uses an ML model to automatically assign a score to each track posted in the r/ProperTechno subreddit. The score describes how likely the track fits the vibe of proper techno. The frontend was built using React, the backend ML model wrapper was built using FastAPI, and the model was trained using scikit-learn. The model was trained using a custom dataset of 1000+ proper techno tracks (downloade thanks to the community spotify playlist and some clandestine libraries that can download tracks directly from streaming services) and 1000+ non-proper techno tracks which I collected from random Techno playlists on spotify that were obviously not 'Proper Techno'. It is a binary classification model that predicts whether a track is proper techno or not.

I plan to extend this in the future and create a Reddit bot that will automatically score the tracks posted in the subreddit in a comment under the post. I have no plans of actioning any direct moderation action using this score, unless the model is really good, then I can probably have it automatically delete or flag posted tracks that don't have a high enough score so us moderators can focus on more important things, like banning trolls and spammers. 

the first iteration of the ML model is using very simple features on the audio data, I will be adding more rich features and improving the model in the near future, but I've got a job and a jiu jitsu career that also needs my focus and attention. So it is what it is. 

## System Architecture Diagram
Add system architecture diagram of Backend and frontend of website..

## Dataset Details

1. Positive cases: Proper Techno spotify playlist -> https://open.spotify.com/playlist/0E6pf5W3NV7armcJYfNK3H?si=826f2122a6b843c8
2. Negative cases: 
    1. DARK /HARD TECHNO: https://open.spotify.com/playlist/1jjzhb9ublCl3X6ZZ6X9kK?si=3ea2988e0b1443e8
    2. ?

## Installation
TBC..