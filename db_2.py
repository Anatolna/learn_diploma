import os
import sqlalchemy
import sys

from sqlalchemy import create_engine
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
#from sqlalchemy.orm import relationship

Base = declarative_base()

class Posts(Base):
    __tablename__ = 'VK_posts'
    user_id = Column(Integer, primary_key=True)
    r_mine = Column(String)
    r_wall = Column(String)

engine = create_engine('sqlite:///posts.db')    
Base.metadata.create_all(engine)
