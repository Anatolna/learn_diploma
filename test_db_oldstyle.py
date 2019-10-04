import sqlalchemy

from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy.orm import mapper

engine = create_engine('sqlite:///:memory:', echo=True)
pool_recycle = 7200

metadata = MetaData()
vk_posts = Table('posts', metadata,
    Column('user_id', Integer, primary_key=True),
    Column('r_mine', String),
    Column('r_wall', String),
)
metadata.create_all(engine)

class Posts(object):
    def __init__(self, user_id, r_mine, r_wall):
        self.user_id = user_id
        self.r_mine = r_mine
        self.r_wall = r_wall
    def __repr__(self):
        return '<Posts user_id {}, {}, {}>'.format(self.user_id, self.r_mine, self.r_wall)

print(mapper (Posts, vk_posts))
post = Posts('123', 'Vasya', 'bla-bla-bla')
print(post)