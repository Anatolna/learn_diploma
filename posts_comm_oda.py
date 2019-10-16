# import vk
import requests
from datetime import datetime
import settings

access_token = settings.access_token
api_version = 5.101
offset = 5
count = 0
# session = vk.Session(access_token=access_token)
# api = vk.API(session, v=api_version)
domain = input('Введите домен сообщества: ')


def posts_collector(access_token, api_version, offset, count, domain):
    posts = []
    # try:
    req_wall = requests.get('https://api.vk.com/method/wall.get', {
                        'domain': domain,
                        'offset': offset,
                        'count': count,  # count - кол-во постов на выходе
                        'access_token': access_token,
                        'v': api_version
                        })
    # except (requests.RequestException, ValueError, TypeError):
    # print('Ошибка ввода. Перепроверьте, что введенный домен существует')
    # print(req_wall.json()["response"]['items'])
    for post in req_wall.json()['response']['items']:
        posts.append({
            'id': post['id'],
            'text': post['text'],
            'date': datetime.fromtimestamp(post['date']).strftime('%d/%m/%y %H:%M')
            })
    return posts
    # print(len(posts))


posts_collector(access_token, api_version, offset, count, domain)


check_inputed = requests.get('https://api.vk.com/method/utils.resolveScreenName',{
                    'screen_name': domain,
                    'access_token': access_token,
                    'v': api_version,
                        })
owner_id = 0 - (check_inputed.json()["response"]['object_id'])
# print(owner_id)


post = input('Введите id поста: ')

def comments_collector(post, access_token, api_version, offset, count, domain, owner_id):
    comments = []
    req_comms = requests.get('https://api.vk.com/method/wall.getComments', {
                        'domain': domain,
                        'offset': offset,
                        'count': count,
                        'access_token': access_token,
                        'v': api_version,
                        'post_id': post,
                        'owner_id': owner_id,
                        })
    # print(req_comms.json()["response"]['items'])
    for comms in req_comms.json()['response']['items']:
        comments.append({
            'post_id': comms['post_id'],
            'comms': comms['text'],
            'date': datetime.fromtimestamp(comms['date']).strftime('%d/%m/%y %H:%M')
            })
    print(comments)
    # return comments

# wow = (554689, 555788, 556333)
# for i in wow:
#     post = i


comments_collector(post, access_token, api_version, offset, count, domain, owner_id)


# if __name__ == "__main__":
