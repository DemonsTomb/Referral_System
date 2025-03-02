from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from pydantic import BaseModel
from typing import List
from .db import get_db
from . import models  # Import the models module

app = FastAPI()
class User(BaseModel):
    id: int
    username: str
    email: str

    class Config:
        orm_mode = True

@app.get("/")
def root():
    return {"message": "FastAPI is running!"}

#sample code to check the connection to the database
@app.get("/health")
def health_check(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))  # Executes a simple query
        return {"status": "Database connected"}
    except Exception as e:
        return {"status": "Database not connected", "error": str(e)}

@app.get("/users", response_model=List[User])
def get_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    if not users:
        raise HTTPException(status_code=404, detail="No users found")
    return users