from fastapi import FastAPI, HTTPException
from models.YoutubeLink import YouTubeLink
from services.predictor import predict 

app = FastAPI()

@app.post("/predict/")
async def predict_track(data: YouTubeLink):
    try:
        # Use the predict function from predictor.py
        score = predict(data.url)  # Pass the YouTube URL directly

        # Return the prediction score
        return {"score": score}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))