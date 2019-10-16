# import os
# import sqlalchemy
# import sys

from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# import settings
import posts_comm_oda
from posts_comm_oda import access_token, api_version, offset, count, domain, owner_id
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
    # date = Column(DateTime)


class Comments(Base):  # # делаем табличку с полями для комментов
    __tablename__ = 'VK_comments'
    id = Column(Integer, primary_key=True)
    id_post = Column(Integer)
    id_comm = Column(Integer)
    comment = Column(String)
    # num_likes = Column(Integer)
    # date = Column(DateTime)


Base.metadata.create_all(engine)
session = sessionmaker(bind=engine)()


posts = posts_comm_oda.posts_collector(access_token, api_version, offset, count, domain)
for entity in posts:
    # all_posts = Posts(id_post=post['id'], post=post['text'], date=post['date'].datetime.strftime('%d-%m-%Y'))
    # comments = comments_collector(post['id'])
    all_posts = Posts(id_post=entity['id'], post=entity['text'])
        # date=datetime.fromtimestamp(entity['date']).strftime('%d/%m/%y %H:%M'))
    session.add(all_posts)
    session.new
    session.commit()


post = input('Введите номер поста: ')
comms = posts_comm_oda.comments_collector(post, access_token, api_version, owner_id, offset, count, domain)
for comment in comms:
    all_comment = Comments(id_post=comment['post_id'], comment=comment['comms'], id_comm=comment['id_comm'])
    session.add(all_comment)
    session.new
    session.commit()
