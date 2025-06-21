from sqlalchemy.orm import Session
from src.models.category_model import Category
from src.models.product_model import Product
from src.schemas.category_schema import CategoryBase, CategoryCreate, CategoryResponse, CategoryUpdate

def get_all_categories(db: Session):
    return db.query(Category).filter(Category.available == True).all()

def create_category(db: Session, category_data: CategoryCreate):
    new_category = Category(**category_data.model_dump())
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category

def get_category_by_id(db: Session, id: int):
    return db.get(Category, id)

def update_category(db: Session, id: int, category_data: CategoryUpdate):
    category = db.get(Category, id)
    if not category:
        return None
    
    update_data = category_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(category, key, value)

    db.commit()
    db.refresh(category)
    return category

def disable_category(db: Session, id: int):
    category = db.get(Category, id)
    if not category:
        return None
    
    if category.id == 1:
        raise ValueError("The 'Undefined' category cannot be disabled")

    db.query(Product).filter(Product.category_id == id).update({Product.category_id: 1})

    category.available = False
    db.commit()
    db.refresh(category)
    return category
