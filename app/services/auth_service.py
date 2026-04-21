from sqlalchemy.orm import Session
from app.models.user import User
from app.core.security import verify_password

def authenticate(db: Session, email: str, password: str):
    # Find user by email
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return None
    # Check password
    if not verify_password(password, user.hashed_password):
        return None
    return user