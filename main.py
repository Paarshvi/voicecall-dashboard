from fastapi import FastAPI, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database import SessionLocal
from models import Call

app = FastAPI()
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class CallCreate(BaseModel):
    customer_name: str
    phone: str


@app.get("/")
def home():
    return {"message": "VoiceCall Dashboard API is running"}


@app.get("/calls")
def get_calls(db: Session = Depends(get_db)):
    calls = db.query(Call).all()
    return calls


@app.post("/calls")
def create_call(call: CallCreate, db: Session = Depends(get_db)):
    new_call = Call(
        customer_name=call.customer_name,
        phone=call.phone,
        status="pending"
    )

    db.add(new_call)
    db.commit()
    db.refresh(new_call)

    return new_call