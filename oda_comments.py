import emoji
import vk
import requests
from datetime import datetime


import settings


access_token = settings.access_token
api_version = 5.101
offset = 0
count = 70
session = vk.Session(access_token=access_token)
api = vk.API(session, v=api_version)
# domain = input('Введите домен сообщества: ')
domain = 'tele2'


def posts_collector(access_token, api_version, offset, count, domain):
    posts = []
    r_wall = requests.get('https://api.vk.com/method/wall.get', {
                        'domain': domain,
                        'offset': offset,
                        'count': count,  # count - кол-во постов на выходе
                        'access_token': access_token,
                        'v': api_version,
                        }
                        )
    # print(r_wall.json()["response"]['items'])
    for post in r_wall.json()['response']['items']:
        posts.append({
            'id': post['id'],
            'text': post['text'],
            'date': post['date'],
            'owner_id': post['owner_id'],
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
    # print('len posts = ', len(posts))
    # print(posts)
    return posts  #, id_posts, date_posts


posts_collector(access_token, api_version, offset, count, domain)

# собираем коменты к посту ()

check_inputed = requests.get('https://api.vk.com/method/utils.resolveScreenName',{
                'screen_name': domain,
                'access_token': access_token,
                'v': api_version,
                    })
owner_id = 0 - check_inputed.json()["response"]['object_id']


# post = input('введите номер поста: ')
post = 565886


def comments_collector(post, access_token, api_version,
                       offset, count, domain, owner_id):
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
    # print(r_comms.json()["response"]['items'])
    for comms in r_comms.json()['response']['items']:
        if 'post_id' in comms.keys():
            comments.append({
                'post_id': comms['post_id'],
                'comms': comms['text'],
                # 'date': post['date'],
                'date': datetime.fromtimestamp(comms['date']).strftime('%d/%m/%y %H:%M')
                })
    # print(comments)
    # print(f'len comments = {len(comments)}')
    return comments


comments_collector(post, access_token, api_version,
                   offset, count, domain, owner_id)

# print(emoji.UNICODE_EMOJI)
emo_comments = comments_collector(post, access_token, api_version,
                   offset, count, domain, owner_id)


def without_emoji_comms(emo_comments):
    comms_with_emo = ''
    for comment in emo_comments:
        comms_with_emo += ''.join(comment['comms'])
    # print(comms_with_emo)
    # non_emoji = ''
    # for symb in alltexts:
    #     if symb in emoji.UNICODE_EMOJI:
    #         non_emoji.replace(symb, '')
    # print(non_emoji)
    comms_without_emo = ''
    for symbol in comms_with_emo:
        if symbol not in emoji.UNICODE_EMOJI:
            comms_without_emo += ''.join(symbol)
    print(comms_without_emo)
    # clean_text = [''.join(words) for words in allsymb]
    # print(clean_text)
    # emoji_list = []
    # for emo in allsymb:
    #     # print(emo)
    #     if emo in emoji.UNICODE_EMOJI:
    #         emoji_list.append(emo)
    # print(emoji_list)
    return comms_without_emo


without_emoji_comms(emo_comments)

# if __name__ == "__main__":
# wow = (565886, 554689, 555788, 556333)
