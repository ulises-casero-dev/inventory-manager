from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from src.schemas.category_schema import CategoryResponse, CategoryCreate, CategoryUpdate
from src.database.database import get_db
from src.services.category_service import(
    get_all_categories as get_all_categories_service,
    create_category as create_category_service,
    get_category_by_id as get_category_by_id_service,
    update_category as update_category_service,
    disable_category as disable_category_service
)

category_router = APIRouter()

@category_router.get('/categories', status_code=200, response_model=List[CategoryResponse], response_description='List of categories')
def get_categories(db: Session = Depends(get_db)):
    categories = get_all_categories_service(db)
    if not categories:
        raise HTTPException(status_code=404, detail='Categories not found')
    return categories

@category_router.get('/categories/{id}', status_code=200, response_model=CategoryResponse, summary='Get a category by id', response_description='Returns a category if it exists')
def get_category_by_id(id: int, db: Session = Depends(get_db)):
    category = get_category_by_id_service(db, id)
    if not category:
        raise HTTPException(status_code=404, detail='Category not found')
    return category

@category_router.post('/categories', status_code=201, response_model=CategoryResponse, summary='Create a new category', description='Adds a new category to the database')
def create_category(category_data: CategoryCreate, db: Session = Depends(get_db)):
    new_category = create_category_service(db, category_data)
    if not new_category:
        raise HTTPException(status_code=400, detail='Error creating category')
    return new_category

@category_router.put('/categories/{id}', status_code=200, summary='Update the information of a category', response_description='Updates the category with the specified ID')
def update_category(id: int, category_data: CategoryUpdate, db: Session = Depends(get_db)):
    category = update_category_service(db, id, category_data)
    if not category:
        raise HTTPException(status_code=404, detail='Category not found')
    return category

@category_router.delete('/categories/{id}', status_code=200, summary='Delete de category', response_description='Logically deletes the category with the specified ID')
def delete_category(id: int, db: Session = Depends(get_db)):
    category = disable_category_service(db, id)
    if not category:
        raise HTTPException(status_code=404, detail='Category not found')
    return category