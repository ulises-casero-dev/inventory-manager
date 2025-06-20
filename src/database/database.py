from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session

URL_DATABASE = 'postgresql://postgres:lalala@localhost:5432/inventory-manager-db'

engine = create_engine(URL_DATABASE)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bimd=engine)

Base: declarative_base()

def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()