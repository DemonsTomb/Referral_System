from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas, auth
from app.database import get_db

router = APIRouter(prefix="/api", tags=["Authentication"])

@router.post("/register")
def register_user(user_data: schemas.UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(models.User).filter(models.User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already in use")

    hashed_password = auth.hash_password(user_data.password)
    new_user = models.User(
        username=user_data.username,
        email=user_data.email,
        password_hash=hashed_password,
        referral_code=user_data.username[:5] + "123"
    )
    
    if user_data.referral_code:
        referrer = db.query(models.User).filter(models.User.referral_code == user_data.referral_code).first()
        if referrer:
            new_user.referred_by = referrer.id
            db.add(models.Referral(referrer_id=referrer.id, referred_user_id=new_user.id, status="successful"))

    db.add(new_user)
    db.commit()
    return {"message": "User registered successfully"}

@router.post("/login")
def login(user_data: schemas.UserLogin, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == user_data.email).first()
    if not user or not auth.verify_password(user_data.password, user.password_hash):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    token = auth.create_access_token({"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}
