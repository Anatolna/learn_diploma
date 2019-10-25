# import os
# import sqlalchemy
# import sys

from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

import posts_comm_oda
from posts_comm_oda import access_token, api_version, offset, count, domain, owner_id, count_comm
# from sqlalchemy.orm import relationship


engine = create_engine('sqlite:///vk_posts_comm.db', echo=True)
"""выбираем, с какой базой хотим работать (sqlite)
и в какой файлик записываем"""
Base = declarative_base()
"""говорим, что это будет декларативный mapping (он удобнее)"""


# access_token = settings.access_token
# api_version = '5.101'
# offset = 30
# count = 2

class Posts(Base):  # делаем табличку с полями для постов
    __tablename__ = 'VK_posts'
    id = Column(Integer, primary_key=True)
    id_post = Column(Integer)
    post = Column(String)
    date_post = Column(DateTime)


class Comments(Base):  # # делаем табличку с полями для комментов
    __tablename__ = 'VK_comments'
    id = Column(Integer, primary_key=True)
    id_post = Column(Integer)
    id_comm = Column(Integer)
    comment = Column(String)
    num_likes = Column(Integer)
    date_comm = Column(DateTime)


Base.metadata.create_all(engine)
session = sessionmaker(bind=engine)()


posts = posts_comm_oda.posts_collector(access_token, api_version,
                                       offset, count, domain)
for entity in posts:
    all_posts = Posts(id_post=entity['id'],
                      post=entity['text'],
                      date_post=datetime.strptime(entity['date_post'], '%d/%m/%y %H:%M'),
                      )
    session.add(all_posts)
    session.new
    session.commit()


# post = input('Введите номер поста: ')
comms_dirty = posts_comm_oda.comments_collector(posts, access_token,
                                                api_version, offset,
                                                count_comm, domain, owner_id)
comms_clean = posts_comm_oda.comms_without_emoji(comms_dirty)                                      
for comment in comms_clean:
    all_comment = Comments(id_post=comment['post_id'],
                           id_comm=comment['id_comm'],
                           comment=comment['comms'],
                           num_likes=comment['count_likes'],
                           date_comm=datetime.strptime(comment['date_comm'], '%d/%m/%y %H:%M'),
                           )
    session.add(all_comment)
    session.new
    session.commit()
