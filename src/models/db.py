from sqlalchemy import Column, create_engine, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Database:
    def __init__(self):
        self.engine = create_engine('postgresql://username:password@localhost/dbname')
        self.connect_db()
    
    def connect_db(self):
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        return Session()
