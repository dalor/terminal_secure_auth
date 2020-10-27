from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    login = Column(String, nullable=False)
    password = Column(String)
    is_admin = Column(Boolean, default=False)
    is_restricted = Column(Boolean, default=False)
    is_check_password = Column(Boolean, default=True)

engine = create_engine('sqlite:///DB.sql')

Session = sessionmaker(bind=engine, autocommit=True)

session = Session()

def create_db():
    Base.metadata.create_all(engine)

def check_table_or_create():
    if not engine.dialect.has_table(engine, 'users'):
        create_db()
    return True

if __name__ == '__main__':
    create_db()
