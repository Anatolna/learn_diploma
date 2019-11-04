from flask import Flask, render_template
# from vkapp.dbdb import Base
from vkapp.parser import posts_collector, comments_collector
from vkapp.parser import access_token, api_version, offset, count, domain, owner_id, posts


def create_app():
    app = Flask(__name__)
    # app.config.from_pyfile('settings.py')
    # Base.init_app(app)

    @app.route('/')
    def show_posts():
        title = 'Статистика группы:'
        get_posts = posts_collector(access_token, api_version,
                                    offset, count, domain)
        # print(get_posts)
        number_likes = 0
        number_pics = 0

        for post in get_posts:
            if post.get('post_pics'):
                number_pics += 1

            number_likes += post['post_likes']

        return render_template('index.html', page_title=title,
                               len_posts=len(get_posts),
                               num_likes=number_likes,
                               num_pics=number_pics,
                               )

    @app.route('/')
    def show_comms():
        get_comms = comments_collector(posts, access_token, api_version,
                                       offset, owner_id)
        num_comm_likes = 0
        for comm in get_comms:
            # print(get_comms)
            num_comm_likes += comm['count_likes']

        return render_template('index.html',
                               len_comms=len(get_comms),
                               comm_likes=num_comm_likes,
                               )

    return app


# potomuchtoludi bolshoitheatre nestearussia
