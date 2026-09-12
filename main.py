from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def home():
    return {"message": "VoiceCall Dashboard API is running"}