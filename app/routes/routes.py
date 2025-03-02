@router.get("/referrals")
def get_referrals(db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    referrals = db.query(models.Referral).filter(models.Referral.referrer_id == user.id).all()
    return {"referrals": referrals}
