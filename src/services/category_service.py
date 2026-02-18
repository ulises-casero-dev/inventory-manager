from sqlalchemy.orm import Session
from sqlalchemy import exists
from src.models.category_model import Category
from src.models.product_model import Product
from src.schemas.category_schema import CategoryBase, CategoryCreate, CategoryResponse, CategoryUpdate
from src.exceptions.custom_exceptions import ConflictException

def get_all_categories(db: Session):
    return db.query(Category).filter(Category.available == True).all()

def create_category(db: Session, category_data: CategoryCreate):

    category_exists = db.query(Category).filter(Category.name == category_data.name).first()

    if category_exists:
        raise ConflictException(
            message="Category with this name already exists.",
            error_code="CATEGORY_ALREADY_EXISTS"
        )

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

    category_exists = db.query(Category).filter(Category.name == category_data.name)
    if category_exists:
        raise ConflictException(
            message="Category with this name already exists.",
            error_code="CATEGORY_ALREADY_EXISTS"
        )
    
    update_data = category_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(category, key, value)

    db.commit()
    db.refresh(category)
    return category


def enable_category(db: Session, id: int):

    category = db.get(Category, id)
    if not category:
        return None

    # comprobar si no esta activa ya
    # if category.active == True:
    # lanzar aviso o error
    # return None

    category.available = False
    db.commit()
    db.refresh(category)
    return category

def disable_category(db: Session, id: int):

    category = db.get(Category, id)
    if not category:
        return None

    #categoria asociada a productos
    product_exists = db.query(exists().where(Product.category_id == id)).scalar()
    if product_exists:
        raise ConflictException(
            message="Category with associated products cannot be disabled",
            error_code="CATEGORY_WITH_PRODUCTS"
        )

    # comprobar si no esta inactiva ya
    #if category.active == False:
        # lanzar aviso o error
        #return None

    if category.id == 1:
        raise ValueError("The 'Undefined' category cannot be disabled")

    category.available = False
    db.commit()
    db.refresh(category)
    return category
