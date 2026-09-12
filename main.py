from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Call(BaseModel):
    customer_name: str
    phone: str


@app.get("/")
def home():
    return {"message": "VoiceCall Dashboard API is running"}


@app.get("/calls")
def get_calls():
    return {"calls": []}


@app.post("/calls")
def create_call(call: Call):
    return {
        "message": "Call created",
        "call": call
    }