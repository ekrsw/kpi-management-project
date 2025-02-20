from .database import BaseDatabase
from sqlalchemy import Column, Integer, String

class Test(BaseDatabase):
    __table__ = "test"
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
