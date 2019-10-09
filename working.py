import csv
import vk
import requests
import vk_api
from datetime import datetime

# тестовый блок по API VK 
# запрос к своему акк
# запрос постов с группы Tele2 \\ сохранено пока в тхт 

access_token = '' #не потерять! это рабочий кей. файл для гит без ключа
api_version = '5.101'
#user_id = 181399036 #ручной
offset = 10
count = 10
session = vk.Session(access_token = access_token)
api = vk.API(session, v = api_version)
# r_mine = requests.get(f'https://api.vk.com/method/users.get?user_ids={user_id}&access_token={access_token}&v={api_version}')
# #print(r_mine.json())

# тащим посты с ВК
r_wall = requests.get(f'https://api.vk.com/method/wall.get?domain=tele2&count={count}&access_token={access_token}&v={api_version}') #count - кол-во постов на выходе
#print(r_wall.json()["response"]['items'])
url = 'https://api.vk.com/method/wall.get?domain=tele2&count=10&offset={offset}&access_token={access_token}&v={api_version}'

# здесь не хватает внешнего ввода параметра domain. думаю что на внешний ин фейс надо выводить именно его. хотя можно, наверное всей ссылкой, но тогда будем придумывать, как вытащить сам домейн из линка
# еще момент: не все группы имеют домейн, бывает просто номер и вот это задачка пока. то есть нужно написать скрипт который меняет параметр в запросе на такие случаи 

# пилим джесон формат, затем засовываем в список словарей их id и сами тексты (требуется чистка от \n)
posts = []
for i in range(0, 15, 5):
    url_formatted = url.format(access_token = access_token, api_version = api_version, offset = i)
    #print(i)
    r_wall = requests.get(url_formatted)
    for post in r_wall.json()["response"]['items']:
        posts.append({
            'id':post['id'],
            'text': post['text']
        })
print(posts)

#добавляем id постов в список словарей, что бы потом к ним обращаться и тянуть коменты

id_posts = [] 
x = (i['id'] for i in posts) 
for post_id in x:
    id_posts.append({
        'id': post_id
    })
print(id_posts)

#собственно  запрос коментов к постам. вроде работает (проверьте), ключ убираю. если надо - кину в личку
# цикл для сбора в файл пока не делала, так как сначала надо решить задачу подстановки id постов в сам запрос
# и тут задачка на подстановку как в запросе на посты: 1 - это id поста (но это решаемо - берем из листа и подставляем), а вот owner_id (он маст) - вот это сложнее, пока не вкурила, но есть мысль
# исключение отсутствие связи - трай-эксепт
# завернуть в функции

# собираем коменты к посту ()
#def comments_posts(id_post):
try:
    post_id=570449 # ну тут либо внешний, либо уже из списка выше
    coms = requests.get(f'https://api.vk.com/method/wall.getComments?domain=tele2&owner_id=-18098621&count=10&offset={offset}&post_id={post_id}&access_token={access_token}&v={api_version}')
    print(coms.json()["response"]['items'])
    url = 'https://api.vk.com/method/wall.getComments?domain=tele2&owner_id=-18098621&count=10&offset={offset}&post_id={post_id}&access_token={access_token}&v={api_version}'
except (requests.RequestException, ValueError, TypeError):
    print('Ошибка запроса')
        #return coms
    #print(coms)

# список словарей постов, вытаскиваем id поста, что мэчить в случае чего с самим постом, комент и дату комента
comments = []
for it in range(0, 15):
    url_formatted = url.format(access_token = access_token, api_version = api_version, offset = i, post_id = post_id)
     #print(i)
    coms = requests.get(url_formatted)
    for coms_info in coms.json()["response"]['items']:
        comments.append({
            'id_post': coms_info['post_id'],
            'date': datetime.fromtimestamp(coms_info['date']).strftime('%d/%m/%y %H:%M'),
            'text': coms_info['text']
        })
print(comments)

# if __name__ == "__main__":
#     r2 = comments_posts('457267757')
#     print(r2)