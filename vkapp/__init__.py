from flask import Flask, flash, redirect, render_template, request, url_for
# from vkapp.dbdb import Base
from vkapp.inputform import Inputform
from vkapp.parser import posts_collector, comments_collector
from vkapp.parser import access_token, api_version, offset, count


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('settings.py')
    # Base.init_app(app)

    @app.route('/')
    def input_domain():
        title = 'Выбор сообщества'
        domain_form = Inputform()
        return render_template('input.html', page_title=title,
                               form=domain_form)

    @app.route('/process_domain', methods=['GET', 'POST'])
    def process_domain():
        form = Inputform()
        domain = form.domain.data

        if form.validate_on_submit():
            print("valid!!!!")
            return redirect(url_for('show_post', domain=domain))
        else:
            # error = 'домен не введен'
            return render_template('input.html', form=form)

    @app.route('/stats/<domain>')
    def show_post(domain=None):
        # print("We are in stats!!!!")
        # print("Domain", domain)
        title = 'Статистика группы'
        get_posts = posts_collector(access_token, api_version,
                                    offset, count, domain)
        number_likes = 0
        number_pics = 0
        number_of_posts = 0
        if get_posts:
            for post in get_posts:
                if post.get('post_pics'):
                    number_pics += 1
                number_likes += post['post_likes']
            number_of_posts = len(get_posts)

        return render_template('index.html', page_title=title,
                               len_posts=number_of_posts,
                               num_likes=number_likes,
                               num_pics=number_pics,
                               )

    # @app.route('/')
    # def show_comms():
    #     get_comms = comments_collector(posts, access_token, api_version,
    #                                    offset, owner_id)
    #     num_comm_likes = 0
    #     for comm in get_comms:
    #         # print(get_comms)
    #         num_comm_likes += comm['count_likes']

    #     return render_template('index.html',
    #                            len_comms=len(get_comms),
    #                            comm_likes=num_comm_likes,
    #                            )

    return app


# potomuchtoludi bolshoitheatre nestearussia
