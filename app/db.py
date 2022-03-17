from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base


engine = create_engine('postgresql://postgres:postgres@0.0.0.0:5432/postgres', echo=True)

Base = declarative_base()
