from flask import Flask, flash, redirect, render_template, url_for
# from vkapp.dbdb import Base
from vkapp.inputform import Inputform
from vkapp.parser import check, comments_collector, is_group, posts_collector
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

    @app.route('/process_domain', methods=['POST'])
    def process_domain():
        form = Inputform()
        domain = form.domain.data
        if is_group(domain, access_token, api_version):
            if form.validate_on_submit():
            # print("valid!!!!")
                return redirect(url_for('show_posts', domain=domain))
        flash('Такого сообщества не существует, попробуйте еще раз')
        return redirect(url_for('input_domain'))
            # return render_template('input.html', form=form)

    @app.route('/<domain>/process_comms', methods=['POST'])
    def process_comms(domain=None):

        # print("process comms form!!!!")
        return redirect(url_for('show_comms', domain=domain))

    @app.route('/stats/<domain>')
    def show_posts(domain=None):
        # print("We are in stats!!!!")
        # print("Domain", domain)
        title = 'Статистика постов'
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
                               domain=domain
                               )

    # @app.route('/process_button/', methods=['GET'])
    # def moving():
    #     submit = Inputbutton()
    #     if submit.validate_on_submit():
    #     return render_template('index.html', form=submit)
    #     return redirect(url_for('show_comms'))

    @app.route('/stats/<domain>/comms')
    def show_comms(domain=None):
        # print("We are in stats!!!!")
        # print("Domain", domain)
        try:
            title = 'Статистика комментов'
            get_posts = posts_collector(access_token, api_version,
                                        offset, count, domain)

            owner_id = check(domain, access_token, api_version)

            get_comms = comments_collector(get_posts, access_token, api_version,
                                           offset, owner_id)
            num_comm_likes = 0
            number_of_comms = 0
            for comm in get_comms:
                # print(get_comms)
                num_comm_likes += comm['count_likes']
                number_of_comms = len(get_comms)

            return render_template('comms.html', page_title=title,
                                   len_comms=number_of_comms,
                                   comm_likes=num_comm_likes,
                                   domain=domain
                                   )
        except(ValueError, KeyError, UnboundLocalError):
            flash('API ВКшки устала и сломалась, попробуйте другое сообщество')
            return redirect(url_for('input_domain'))

    return app


# potomuchtoludi bolshoitheatre nestearussia antipremia redcircule code.help
