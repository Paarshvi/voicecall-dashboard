from fastapi import FastAPI, Depends
from pydantic import BaseModel
from enum import Enum
from sqlalchemy.orm import Session

from database import SessionLocal
from models import Call
from call_queue import call_queue
from worker import process_call

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

class CallStatus(str, Enum):
    pending = "pending"
    processing = "processing"
    completed = "completed"
    failed = "failed"
    retrying = "retrying"

class CallStatusUpdate(BaseModel):
    status: CallStatus

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

    call_queue.enqueue(process_call, new_call.id)

    return new_call

@app.patch("/calls/{call_id}")
def update_call_status(
    call_id: int,
    status_update: CallStatusUpdate,
    db: Session = Depends(get_db)
):
    call = db.query(Call).filter(Call.id == call_id).first()

    if not call:
        return {"message": "Call not found"}

    call.status = status_update.status

    db.commit()
    db.refresh(call)

    return call

@app.delete("/calls/{call_id}")
def delete_call(call_id: int, db: Session = Depends(get_db)):
    call = db.query(Call).filter(Call.id == call_id).first()

    if not call:
        return {"message": "Call not found"}

    db.delete(call)
    db.commit()

    return {"message": "Call deleted"}