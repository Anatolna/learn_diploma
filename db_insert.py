from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db_2 import Base, Posts

engine = create_engine('sqlite:///posts.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

new_post = Posts(r_mine = 'abcde', r_wall = 'qwertyuio')
session.add(new_post)
session.commit()