from db.database import Base , engine
from models.user import User

def init_db():
    Base.metadata.create_all(bind=engine)
