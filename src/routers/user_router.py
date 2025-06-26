from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from src.database.database import get_db
from src.schemas.user_schema import UserCreate, UserUpdate, UserResponse
from src.services.user_service import (
    get_all_users as get_all_users_service,
    get_user_by_id as get_user_by_id_service,
    create_user as create_user_service,
    update_user as update_user_service,
    deactivate_user as deactivate_user_service
)

user_router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@user_router.get('/users', status_code=200, response_model=List[UserResponse], response_description='List of users')
def get_users(db: Session = Depends(get_db)):
    users = get_all_users_service(db)
    if not users:
        raise HTTPException(status_code=404, detail='Users not found')
    return users

@user_router.get('/users/{id}', status_code=200, response_model=UserResponse, summary='Get user by id', response_description='Returns a user if it exist')
def get_user_by_id(id: int, db: Session = Depends(get_db)):
    user = get_user_by_id_service(db, id)
    if not user:
        raise HTTPException(status_code=404, detail='User not found')
    return user

@user_router.post('/users', status_code=201, response_model=UserResponse, summary='Create a new user', description='Adds a new user to de database')
def create_user(user_data: UserCreate, db: Session = Depends(get_db)):
    new_user = create_user_service(db, user_data)
    return new_user

@user_router.put('/users/{id}', status_code=200, summary='Updates the information of a user', response_description='Updates the user with the specified ID')
def update_user(id:int, user_data: UserUpdate, db: Session = Depends(get_db)):
    user = update_user_service(id, user_data, db)
    if not user:
        raise HTTPException(status_code=404, detail='User not found')
    return user

@user_router.delete('/users/{id}', status_code=200, summary='Delete user', response_description='Logically deletes the user with the specified ID')
def delete_user(id: int, db: Session = Depends(get_db)):
    user = deactivate_user_service(id, db)
    if not user:
        raise HTTPException(status_code=404, detail='User not found')
    return user    