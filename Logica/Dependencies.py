from sqlalchemy.orm import Session
from Conexion.DataBase import SessionLocal

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
