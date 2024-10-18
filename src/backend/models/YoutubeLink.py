from pydantic import BaseModel

class YouTubeLink(BaseModel):
    url: str