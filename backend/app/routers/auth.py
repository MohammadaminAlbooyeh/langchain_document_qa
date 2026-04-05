from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schemas.user import UserCreate, UserOut
from app.models.user import User
from app.core.deps import get_db
from app.core.security import get_password_hash, verify_password, create_access_token

router = APIRouter()


@router.post("/register", response_model=UserOut)
def register(payload: UserCreate, db: Session = Depends(get_db)):
    user = db.query(User).filter((User.username == payload.username) | (User.email == payload.email)).first()
    if user:
        raise HTTPException(status_code=400, detail="user exists")
    new = User(username=payload.username, email=payload.email, hashed_password=get_password_hash(payload.password))
    db.add(new)
    db.commit()
    db.refresh(new)
    return new


@router.post("/login")
def login(payload: UserCreate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == payload.username).first()
    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="invalid credentials")
    token = create_access_token({"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}
