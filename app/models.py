from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from .db import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    referral_code = Column(String, unique=True, nullable=False)
    referred_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    referrals = relationship("Referral", back_populates="referrer", foreign_keys="[Referral.referrer_id]")

    class Config:
        orm_mode = True

class Referral(Base):
    __tablename__ = "referrals"

    id = Column(Integer, primary_key=True, index=True)
    referrer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    referred_user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    status = Column(String, default="pending")
    date_referred = Column(DateTime, default=datetime.utcnow)

    referrer = relationship("User", back_populates="referrals", foreign_keys=[referrer_id])
    referred_user = relationship("User", foreign_keys=[referred_user_id])