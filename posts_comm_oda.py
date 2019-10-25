import emoji
import requests
from datetime import datetime
import time
import settings


access_token = settings.API_KEY
api_version = 5.101
offset = 0
count = 10
domain = input('Введите домен сообщества: ')
# domain = 'tele2'


def posts_collector(access_token, api_version, offset, count, domain):
    posts = []
    for offset in range(0, 100, 100):  # добавила цикл, чтобы получать больше 100 постов
        req_wall = requests.get('https://api.vk.com/method/wall.get', {
                    'domain': domain,
                    'offset': offset,
                    'count': count,  # count - кол-во постов на выходе
                    'access_token': access_token,
                    'v': api_version
                    })
    # member_count = req_wall.json()['response']['count']
    # except(requests.ConnectionError):
    # print(req_wall.json()["response"]['items'])
    # print("total members = ", member_count)
    # except (requests.RequestException, ValueError, TypeError):
        # print('Ошибка ввода. Перепроверьте, что введенный домен существует')
        time.sleep(0.5)
        got_posts = req_wall.json()['response']['items']
        for post in got_posts:
            posts.append({
                'id': post['id'],
                'text': post['text'],
                'date_post': datetime.fromtimestamp(post['date']).strftime('%d/%m/%y %H:%M'),
                'owner_id': post['owner_id'],
                })
        print('len posts = ', len(posts))
    # else:
    #     print('Проверьте корректность ввода домена')
    # print(posts)
    return posts


# posts_collector(access_token, api_version, offset, count, domain)


check_inputed = requests.get('https://api.vk.com/method/utils.resolveScreenName', {
                    'screen_name': domain,
                    'access_token': access_token,
                    'v': api_version,
                    })

owner_id = 0 - (check_inputed.json()["response"]['object_id'])
# print("ID!!!!!!!!", owner_id)


# post = input('Введите id поста: ')
count_comm = 100
posts = posts_collector(access_token, api_version, offset, count, domain)


def choose_numbers_comments(num_comm):
    num_comm = input("""Введите 1, если вы хотите выгрузить все комментарии,
                        или 2, если хотите ввести номер поста""")
    if num_comm == 1:
        return 'Выгружаем все комменты сообщества'
    else:
        return 'Введите ID поста'


def comments_collector(posts, access_token, api_version,
                       offset, count_comm, domain, owner_id):
    comments = []
    for post in posts:
        req_comms = requests.get('https://api.vk.com/method/wall.getComments', {
                            'domain': domain,
                            'offset': offset,
                            'count': count_comm,  # у комментов свой count!
                            'access_token': access_token,
                            'v': api_version,
                            'post_id': post['id'],
                            'owner_id': post['owner_id'],
                            'need_likes': 1
                            })
    # print(req_comms.json()["response"]['items'])
        # for offset in range(0, 10):
        time.sleep(0.5)
        all_comments = req_comms.json()['response']['items']
        # print("ALL!!!!!!!", len(all_comments))
        for comms in all_comments:
            if 'post_id' in comms.keys():  # берем только комменты, где есть post_id (и текст)
                comments.append({
                    'post_id': comms['post_id'],
                    'id_comm': comms['id'],
                    'comms': comms['text'],
                    'count_likes': comms['likes']['count'],
                    'date_comm': datetime.fromtimestamp(comms['date']).strftime('%d/%m/%y %H:%M'),
                    })
    # print(comments)
    # print(f'len comments = {len(comments)}')
    return comments


# comments_collector(posts, access_token, api_version,
#                    offset, count_comm, domain, owner_id)


def filter_comments(all_comments):
    long_comments = []
    for cccc in all_comments:
        if len(cccc['comms']) > 7:
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


if __name__ == "__main__":
    print('все отработано')


# wow = (565886, 554689, 555788, 556333)
