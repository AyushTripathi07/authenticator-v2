from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from db.constants import PSQL_USER , PSQL_DB , PSQL_HOST , PSQL_PASSWORD

DATABASE_URL = f"postgresql://{PSQL_USER}:{PSQL_PASSWORD}@{PSQL_HOST}:5432/{PSQL_DB}"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit =False,autoflush=False,bind=engine)

Base = declarative_base()
