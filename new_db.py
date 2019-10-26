import os
# import sqlalchemy
# import sys

from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

import oda_comments
from oda_comments import access_token, api_version, offset, count, domain, owner_id
# from sqlalchemy.orm import relationship


os.remove(r"db_test.db")


engine = create_engine('sqlite:///db_test.db', echo=True)
"""выбираем, с какой базой хотим работать (sqlite)
и в какой файлик записываем"""
Base = declarative_base()
"""говорим, что это будет декларативный mapping (он удобнее)"""


class Posts(Base):  # делаем табличку с полями для постов
    __tablename__ = 'VK_posts'
    id = Column(Integer, primary_key=True)
    id_post = Column(Integer)
    likes = Column(Integer)
    pics = Column(Boolean)
    post = Column(String)
    date = Column(DateTime)


class Comments(Base):  # # делаем табличку с полями для комментов
    __tablename__ = 'VK_comments'
    id = Column(Integer, primary_key=True)
    id_post = Column(Integer)
    id_comm = Column(Integer)
    comment = Column(String)
    num_likes = Column(Integer)
    date = Column(DateTime)


Base.metadata.create_all(engine)
session = sessionmaker(bind=engine)()


posts = oda_comments.posts_collector(access_token, api_version,
                                     offset, count, domain)
for entity in posts:
    all_posts = Posts(id_post=entity['id'],
                      likes=entity['post_likes'],
                      post=entity['text'],
                      date=datetime.strptime(entity['date'], '%d/%m/%y %H:%M'),
                      pics=entity['post_pics'],
                      )
    session.add(all_posts)
    session.new
    session.commit()


# post = input('введите номер поста: ')
post = 572920
comments_dirty = oda_comments.comments_collector(post, access_token,
                                                 api_version, offset,
                                                 count, domain, owner_id)
comms_clean = oda_comments.comms_without_emoji(comments_dirty)
for comment in comms_clean:
    all_comment = Comments(id_post=comment['post_id'],
                           id_comm=comment['id_comms'],
                           comment=comment['comms'],
                           num_likes=comment['count_likes'],
                           date=datetime.strptime(comment['date_comm'], '%d/%m/%y %H:%M'),
                           )
    session.add(all_comment)
    session.new
    session.commit()
