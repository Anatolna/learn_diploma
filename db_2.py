import os
import sqlalchemy
import sys

from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
#from sqlalchemy.orm import relationship

Base = declarative_base()

class Posts(Base):
    __tablename__ = 'VK_posts_comments'
    id_post = Column(Integer, primary_key=True)
    post = Column(String)
    id_comm = Column(Integer)
    comment = Column(String)
    num_likes = Column(Integer)
    date = Column(DateTime)


engine = create_engine('sqlite:///vk_posts.db')
Base.metadata.create_all(engine)