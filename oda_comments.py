import emoji
import vk
import requests
import time
from datetime import datetime


import settings


access_token = settings.API_KEY
api_version = 5.101
offset = 0
count = 99
session = vk.Session(access_token=access_token)
api = vk.API(session, v=api_version)
domain = input('Введите домен сообщества: ')
# domain = 'tele2'


def is_group(domain, access_token, api_version):
    # domain = input('Введите домен сообщества: ')
    check_url = 'https://api.vk.com/method/utils.resolveScreenName'
    check_inputed = requests.get(check_url, {
                'screen_name': domain,
                'access_token': access_token,
                'v': api_version,
                    })
    # print(check_inputed)
    ans = check_inputed.json()["response"]
    # print(ans)
    # for domain in ans:
    if ans:
        # if 'type' not in ans:
        if ans['type'] != 'group':
            print(f"Ошибка домена, проверьте имя сообщества {ans['type']}")
            return
            
    else:
        print('такого объекта нет')
        return
            # owner_id = False
    # except:
    #     owner_id = 0 - ans['object_id']
    # print(owner_id)        
    return domain  # , owner_id


# is_group(domain, access_token, api_version)


def posts_collector(access_token, api_version, offset, count, domain):
    if is_group(domain, access_token, api_version):
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
        time.sleep(0.5)
        itemes = r_wall.json()['response']['items']
        for post in itemes:
            dict_post = {
                'id': post['id'],
                'text': post['text'],
                # 'date_post': post['date'],
                'owner_id': post['owner_id'],
                'post_likes': post['likes']['count'],
                'date': datetime.fromtimestamp(post['date'])\
                .strftime('%d/%m/%y %H:%M')
                }
            # print(post.keys())
            if post.get('attachments'):
            # if 'attachments' in post:
                attachments = post['attachments']
                for attach in attachments:
                    if attach['type'] == 'photo':
                        # print(post)
                        dict_post['post_pics'] = True
                    else:
                        dict_post['post_pics'] = False
            posts.append(dict_post)
        print('число постов = ', len(posts))
        return posts


posts_collector(access_token, api_version, offset, count, domain)

# собираем коменты к посту ()
"""
check_inputed = requests.get('https://api.vk.com/method/utils.resolveScreenName',{
                'screen_name': domain,
                'access_token': access_token,
                'v': api_version,
                    })
owner_id = 0 - check_inputed.json()["response"]['object_id']


# post = input('введите номер поста: ')
post = 572920
# post = posts_collector(access_token, api_version, offset, count, domain)


def comments_collector(post, access_token, api_version,
                       offset, count, domain, owner_id):
    comments = []
    for offset in range(0, 5):
        # for one_post in post:
        r_comms = requests.get('https://api.vk.com/method/wall.getComments', {
                            'domain': domain,
                            'offset': offset,
                            'count': count,
                            'access_token': access_token,
                            'v': api_version,
                            'post_id': post,
                            'owner_id': owner_id,
                            'need_likes': 1,
                            }
                            )
    # print(len(r_comms.json()["response"]['items']))
        time.sleep(0.5)
        all_comms = r_comms.json()['response']['items']
        for comms in all_comms:
            if 'post_id' in comms.keys():
                comments.append({
                    'post_id': comms['post_id'],
                    'comms': comms['text'],
                    'id_comms': comms['id'],
                    'count_likes': comms['likes']['count'],
                    # 'date': post['date'],
                    'date_comm': datetime.fromtimestamp(comms['date']).strftime('%d/%m/%y %H:%M')
                    })
    # print(comments)
    # print(f'len comments = {len(comments)}')
    return comments


# comments_collector(post, access_token, api_version,
                #    offset, count, domain, owner_id)


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


# comms_with_emo = comments_collector(post, access_token, api_version,
                                    # offset, count, domain, owner_id)
# print(comms_without_emoji(comms_with_emo))


# if __name__ == "__main__":
# wow = (565886, 554689, 555788, 556333)
"""