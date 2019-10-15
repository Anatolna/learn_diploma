import vk
import requests
from datetime import datetime


import settings


access_token = settings.access_token
api_version = 5.101
offset = 0
count = 7
session = vk.Session(access_token=access_token)
api = vk.API(session, v=api_version)
domain = input('Введите домен сообщества: ')


def posts_collector(access_token, api_version, offset, count, domain):
    posts = []
    r_wall = requests.get('https://api.vk.com/method/wall.get', {
                        'domain': domain,
                        'offset': offset,
                        'count': count,  # count - кол-во постов на выходе
                        'access_token': access_token,
                        'v': api_version
                        }
                        )
    # print(r_wall.json()["response"]['items'])
    for post in r_wall.json()['response']['items']:
        posts.append({
            'id': post['id'],
            'text': post['text'],
            'date': post['date'],
            # 'date': datetime.fromtimestamp(post['date']).strftime('%d/%m/%y %H:%M')
            })
    # id_posts = []
    # x = (i['id'] for i in posts)
    # for post_id in x:
    #     id_posts.append({
    #         'id': post_id
    #     })
    # date_posts = []
    # d = (i['date'] for i in posts)
    # for post_date in d:
    #     date_posts.append({
    #         'date': post_date
    #     })
    return posts  #, id_posts, date_posts
    # print(posts)


posts_collector(access_token, api_version, offset, count, domain)

# собираем коменты к посту ()

check_inputed = requests.get('https://api.vk.com/method/utils.resolveScreenName',{
                'screen_name': domain,
                'access_token': access_token,
                'v': api_version,
                    })
owner_id = 0 - check_inputed.json()["response"]['object_id']


post = input('введите номер поста: ')
def comments_collector(post, access_token, api_version, offset, count, domain, owner_id):
    comments = []
    r_comms = requests.get('https://api.vk.com/method/wall.getComments', {
                        'domain': domain,
                        'offset': offset,
                        'count': count,
                        'access_token': access_token,
                        'v': api_version,
                        'post_id': post,
                        'owner_id': owner_id,
                        }
                        )
    print(r_comms.json()["response"]['items'])
    for comms in r_comms.json()['response']['items']:
        comments.append({
            'post_id': comms['post_id'],
            'comms': comms['text'],
            # 'date': post['date'],
            # 'date': datetime.fromtimestamp(post['date']).strftime('%d/%m/%y %H:%M')
            })
    # print(len(comments))
    return comments


comments_collector(post, access_token, api_version, offset, count, domain, owner_id)


# if __name__ == "__main__":
