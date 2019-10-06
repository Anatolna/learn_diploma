from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db_2 import Base, Posts

engine = create_engine('sqlite:///vk_posts.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

new_post = Posts(id_post = 123, post = 'qwertyuio', id_comm = 777, comment = 'фываолдж', num_likes = 5, date = datetime.now())
session.add(new_post)
session.commit()