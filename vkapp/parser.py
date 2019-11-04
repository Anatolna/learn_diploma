import emoji
from datetime import datetime
from flask import current_app
import requests
import time
import vkapp.settings


access_token = vkapp.settings.API_KEY
api_version = 5.101
offset = 0
count = 100
domain = 'potomuchtoludi'
# domain = input('Введите сообщество: ')
# owner_id_inputed = input('Введите сообщество: ')


def is_group(domain, access_token, api_version):
    # проверка ввода domain
    try:
        check_url = 'https://api.vk.com/method/utils.resolveScreenName'
        check_inputed = requests.get(check_url, {
                    'screen_name': domain,
                    'access_token': access_token,
                    'v': api_version,
                        })
        # owner_id = 0 - check_inputed.json()["response"]['object_id']
        # print(check_inputed)
        check_inputed.raise_for_status()
        ans = check_inputed.json()["response"]
        # print(ans)
        if ans:
            # if 'type' not in ans:
            if ans['type'] != 'group':
                print(f"Ошибка домена, проверьте имя, сейчас это {ans['type']}")
                return
        else:
            print('Такого сообщества нет, проверьте имя домена')
            return
    except(requests.RequestException, ValueError, KeyError):
        print('Ошибка сети')
        return False
    return domain  # , owner_id


# is_group(domain, access_token, api_version)


def posts_collector(access_token, api_version, offset, count, domain):
    if is_group(domain, access_token, api_version):
        posts = []
        post_read = 0
        try:
            req_wall = requests.get('https://api.vk.com/method/wall.get', {
                        'domain': domain,
                        # 'owner_id': owner_id,
                        'offset': 0,
                        'count': 1,
                        'access_token': access_token,
                        'v': api_version,
                        'extended': 1              
                        })
            req_wall.raise_for_status()
            wall_post_number = req_wall.json()['response']['count']
            # print(wall_post_number)
            while post_read < wall_post_number:
                req_wall = requests.get('https://api.vk.com/method/wall.get', {
                        'domain': domain,
                        # 'owner_id': owner_id,
                        'offset': post_read,
                        'count': count,
                        'access_token': access_token,
                        'v': api_version,
                        'extended': 1
                        })
                time.sleep(0.5)
                req_wall.raise_for_status()
                got_posts = req_wall.json()['response']['items']
                for post in got_posts:
                    if 'likes' in post.keys():
                        dict_post = {
                                'id': post['id'],
                                'text': post['text'],
                                'owner_id': post['owner_id'],
                                'post_likes': post['likes']['count'],
                                'date': datetime.fromtimestamp(post['date'])
                                .strftime('%d/%m/%y %H:%M')
                                }
                # print(post.keys())
                    if post.get('attachments'):
                        attachments = post['attachments']
                        for attach in attachments:
                            if attach['type'] == 'photo':
                                dict_post['post_pics'] = True
                            else:
                                dict_post['post_pics'] = False
                    else:
                        dict_post['post_pics'] = False
                    posts.append(dict_post)
                post_read += len(got_posts)
        except(requests.RequestException, ValueError):
            print('Ошибка сети')
            return False
        # print(post_read)
        # print(posts)
        # print('len posts = ', len(posts))
        return posts


# posts_collector(access_token, api_version, offset, count, domain)

def check(domain, access_token, api_version):
    try:
        check_inputed = requests.get('https://api.vk.com/method/utils.resolveScreenName', {
                'screen_name': domain,
                'access_token': access_token,
                'v': api_version,
                })
        owner_id = 0 - check_inputed.json()["response"]['object_id']
        # print(owner_id)
    except (requests.RequestException, ValueError):
        print('Сетевая ошибка')
    return owner_id


posts = posts_collector(access_token, api_version, offset, count, domain)


def comments_collector(posts, access_token, api_version, offset, owner_id):
    comments = []
    for post in posts:
        req_comms = requests.get('https://api.vk.com/method/wall.getComments', {
                            # 'domain': domain,
                            'offset': 0,
                            'count': 100,
                            'access_token': access_token,
                            'v': api_version,
                            'post_id': post['id'],
                            'owner_id': post['owner_id'],
                            'need_likes': 1
                            })
        time.sleep(0.5)
        wall_comm_number = req_comms.json()['response']['count']
        if wall_comm_number != 0:
            comm_read = len(req_comms.json()['response']['items'])
            # print('len(comm_read) = ', comm_read)
            # print(req_comms.json()['response']['items'])
            all_comments = req_comms.json()['response']['items']
            for comms in all_comments:
                if comms['thread']['count'] > 0:
                    req_comms = requests.get('https://api.vk.com/method/wall.getComments', {
                                # 'domain': domain,
                                'offset': 0,
                                'count': 100,
                                'access_token': access_token,
                                'v': api_version,
                                'post_id': post['id'],
                                'comment_id': comms['id'],
                                'owner_id': post['owner_id'],
                                'need_likes': 1
                                })
                    time.sleep(0.8)
                    thread_comments = req_comms.json()['response']['items']
                    for thread_comms in thread_comments:
                        comments.append({
                            'post_id': thread_comms['post_id'],
                            'id_comm': thread_comms['id'],
                            'comms': thread_comms['text'],
                            'count_likes': thread_comms['likes']['count'],
                            'date': datetime.fromtimestamp(thread_comms['date']).strftime('%d/%m/%y %H:%M')
                            })
                    comm_read += comms['thread']['count']
                if 'post_id' in comms.keys():  # берем только комменты, где есть post_id (и текст)
                    comments.append({
                        'post_id': comms['post_id'],
                        'id_comm': comms['id'],
                        'comms': comms['text'],
                        'count_likes': comms['likes']['count'],
                        'date': datetime.fromtimestamp(comms['date']).strftime('%d/%m/%y %H:%M')
                        })
            while comm_read < wall_comm_number:
                time.sleep(0.5)
                req_comms = requests.get('https://api.vk.com/method/wall.getComments', {
                                # 'domain': domain,
                                'offset': comm_read,
                                'count': 100,
                                'access_token': access_token,
                                'v': api_version,
                                'post_id': post['id'],
                                'owner_id': post['owner_id'],
                                'need_likes': 1
                                })
                all_comments = req_comms.json()['response']['items']
                # print('len(all_comments) = ', len(all_comments))
                for comms in all_comments:
                    if comms['thread']['count'] > 0:
                        req_comms = requests.get('https://api.vk.com/method/wall.getComments', {
                                    # 'domain': domain,
                                    'offset': 0,
                                    'count': 100,
                                    'access_token': access_token,
                                    'v': api_version,
                                    'post_id': post['id'],
                                    'comment_id': comms['id'],
                                    'owner_id': post['owner_id'],
                                    'need_likes': 1
                                    })
                        time.sleep(0.5)
                        thread_comments = req_comms.json()['response']['items']
                        for thread_comms in thread_comments:
                            comments.append({
                                'post_id': thread_comms['post_id'],
                                'id_comm': thread_comms['id'],
                                'comms': thread_comms['text'],
                                'count_likes': thread_comms['likes']['count'],
                                'date': datetime.fromtimestamp(thread_comms['date']).strftime('%d/%m/%y %H:%M')
                                })
                        comm_read += comms['thread']['count']
                    if 'post_id' in comms.keys():
                        comments.append({
                            'post_id': comms['post_id'],
                            'id_comm': comms['id'],
                            'comms': comms['text'],
                            'count_likes': comms['likes']['count'],
                            'date': datetime.fromtimestamp(comms['date']).strftime('%d/%m/%y %H:%M')
                            })
                comm_read += len(all_comments)
            # print('post ok')
    # print(f'len comments = {len(comments)}')
    return comments


# comments_collector(posts, access_token, api_version, offset, owner_id)


def filter_comments(all_comments):
    long_comments = []
    for cccc in all_comments:
        if len(cccc['comms']) > 2:
            long_comments.append(cccc)
    return long_comments


def comms_without_emoji(list_comms):
    result = []
    long_comment_from_list_comms = filter_comments(list_comms)
    for comment in long_comment_from_list_comms:
        comment_text = comment['comms']
        for symbol in comment_text:
            if symbol in emoji.UNICODE_EMOJI.keys():
                comment_text = comment_text.replace(symbol, '')
        # print(comment_text)
        new_comment = comment
        new_comment['comms'] = comment_text
        result.append(new_comment)
    # print(result)
    return result


# comms_with_emo = comments_collector(posts, access_token, api_version,
# offset, owner_id)
# print(comms_without_emoji(comms_with_emo))


def show_posts():
    get_posts = posts_collector(access_token, api_version,
                                offset, count, domain)
    # print(get_posts)
    number_likes = 0
    number_pics = 0

    for post in get_posts:
        if post.get('post_pics'):
            number_pics += 1

        number_likes += post['post_likes']
    return 


if __name__ == "__main__":
    print('все отработано')
