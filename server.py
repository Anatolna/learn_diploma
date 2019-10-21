from flask import Flask
from posts_comm_oda import posts_collector


app = Flask(__name__)

@app.route('/')
def index():
    posts = posts_collector('tele2')
    return f'ID поста: {posts[post['id']]}, Текст поста: {posts['text']}'

if __name__ == '__main__':
    app.run()
