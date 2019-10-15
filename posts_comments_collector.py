import vk
import requests
from datetime import datetime
import settings

access_token = settings.API_KEY
api_version = 5.101
offset = 1
count = 2 # сделать каунт отдельно к постам и комментам. 0 выгружает все, поэтому для теста стоит пока 2!!! не менять

domain = input('Введите домен сообщества: ')

check_inputed = requests.get('https://api.vk.com/method/utils.resolveScreenName',{
                    'screen_name': domain,
                    'access_token': access_token,
                    'v': api_version,
                        })
owner_id = 0 - (check_inputed.json()["response"]['object_id'])
print(owner_id)

#def posts_collector(access_token, api_version, offset, count, domain):
posts = []
    #try:
req_wall = requests.get('https://api.vk.com/method/wall.get', {
                    'domain': domain,
                    'offset': offset,
                    'count': count,
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
    #return posts
    #print(posts) 
#posts_collector(access_token, api_version, offset, count, domain)

  
list_of_post_id = list()
for number_set in posts:
    list_of_post_id.append(number_set['id'])
print(list_of_post_id) 


# def comments_collector(post, access_token, api_version, offset, count, domain, owner_id):

comments = []
for number in list_of_post_id:
    req_comms = requests.get('https://api.vk.com/method/wall.getComments', {
        'domain': domain,
        'offset': offset,
        'count': count,
        'access_token': access_token,
        'v': api_version,
        'post_id': number,
        'owner_id': owner_id,
        })
    # print(req_comms.json()["response"]['items'])
    for comms in req_comms.json()['response']['items']:
        comments.append({
        'post_id': comms['post_id'],
        'comms': comms['text'],
        'date': datetime.fromtimestamp(comms['date']).strftime('%d/%m/%y %H:%M'),
        })
print(comments)
    #return comments

# comments_collector(post, access_token, api_version, offset, count, domain, owner_id)


# if __name__ == "__main__": 
#     token = ""  
#     session = vk.Session(access_token=token)
#     vk_api = vk.API(session)