from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session

URL_DATABASE = 'postgresql+psycopg2://postgres:lalala@localhost:5432/inventory-manager-db'

engine = create_engine(URL_DATABASE, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()