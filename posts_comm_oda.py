import requests
from datetime import datetime
import time
import settings


access_token = settings.access_token
api_version = 5.101
offset = 0
count = 100
# domain = input('Введите домен сообщества: ')
domain = 'tele2'


def posts_collector(access_token, api_version, offset, count, domain):
    posts = []
    # try:
    for offset in range(0, 500, 100):  # добавила цикл, чтобы получать больше, чем 100 постов
        req_wall = requests.get('https://api.vk.com/method/wall.get', {
                    'domain': domain,
                    'offset': offset,
                    'count': count,  # count - кол-во постов на выходе
                    'access_token': access_token,
                    'v': api_version
                    })
    # except(requests.ConnectionError):
    #     print('Сетевая ошибка')
    #     return False
    # return False
    # print(req_wall.json()["response"]['items'])
    # member_count = req_wall.json()['response']['count']
    # print("total members = ", member_count)
    # except (requests.RequestException, ValueError, TypeError):
        # print('Ошибка ввода. Перепроверьте, что введенный домен существует')
        time.sleep(0.5)
        for post in req_wall.json()['response']['items']:
            posts.append({
                'id': post['id'],
                'text': post['text'],
                'date': datetime.fromtimestamp(post['date']).strftime('%d/%m/%y %H:%M')
                })
    print('len posts = ', len(posts))
    # print(posts)
    return posts


posts_collector(access_token, api_version, offset, count, domain)


check_inputed = requests.get('https://api.vk.com/method/utils.resolveScreenName', {
                    'screen_name': domain,
                    'access_token': access_token,
                    'v': api_version,
                    })
owner_id = 0 - (check_inputed.json()["response"]['object_id'])
# print(owner_id)


post = input('Введите id поста: ')
count_comm = 100


def comments_collector(post, access_token, api_version, offset, count_comm, domain, owner_id):
    comments = []
    for offset in range(0, 300, 100):
        req_comms = requests.get('https://api.vk.com/method/wall.getComments', {
                            'domain': domain,
                            'offset': offset,
                            'count': count_comm,  # у комментов свой count!
                            'access_token': access_token,
                            'v': api_version,
                            'post_id': post,
                            'owner_id': owner_id,
                            })
    # print(req_comms.json()["response"]['items'])
        time.sleep(0.5)
        for comms in req_comms.json()['response']['items']:
            if 'post_id' in comms.keys():  # берем только комменты, где есть post_id (и текст)
                comments.append({
                    'post_id': comms['post_id'],
                    'comms': comms['text'],
                    'date': datetime.fromtimestamp(comms['date']).strftime('%d/%m/%y %H:%M')
                    })
    # print(comments)
    print(f'len comments = {len(comments)}')
    return comments

# wow = (565886, 554689, 555788, 556333)
# for i in wow:
#     post = i


comments_collector(post, access_token, api_version, offset, count_comm, domain, owner_id)


if __name__ == "__main__":
    print('все отработано')
