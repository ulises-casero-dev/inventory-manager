from sqlalchemy.orm import Session
from src.models.user_model import User
from src.schemas.user_schema import UserCreate, UserUpdate

def get_all_users(db: Session):
    return db.query(User).filter(User.active == True).all()

def get_user_by_id(db: Session, id: int):
    return db.get(User, id)

def create_user(db: Session, user_data: UserCreate):
    new_user = User(**user_data.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def update_user(db: Session, id: int, user_data: UserUpdate):
    user = db.get(User, id)
    if not user:
        return None
    update_data = user_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(user, key, value)

    db.commit()
    db.refresh(user)
    return user

def deactivate_user(db: Session, id: int):
    user = db.get(User, id)
    if not user:
        return None
    
    user.active = False
    db.commit()
    db.refresh(user)
    return user