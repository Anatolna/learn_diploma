import csv
import vk
import requests
import vk_api

# тестовый блок по API VK
# запрос к своему акк
# запрос постов с группы ТРЦ в Краснодаре \\ сохранено пока в тхт 

access_token = '-----------' #не похерь! это сука рабочий кей. файл для гит без ключа
api_version = '5.101'
user_id = 181399036 #ручной
numb = 10 # запилить под ручной ввод + domain
offset = 20
session = vk.Session(access_token = access_token)
api = vk.API(session, v = api_version)
r_mine = requests.get(f'https://api.vk.com/method/users.get?user_ids={user_id}&access_token={access_token}&v={api_version}')
#print(r_mine.json())
r_wall = requests.get(f'https://api.vk.com/method/wall.get?domain=nskgallery&count={numb}&access_token={access_token}&v={api_version}') #count - кол-во постов на выходе
#print(r_wall.json()["response"]['items'][1])
url = 'https://api.vk.com/method/wall.get?domain=nskgallery&count={numb}&offset={offset}&access_token={access_token}&v={api_version}'
texts = []

for i in range(0, 11): 
    url_formatted = url.format(access_token = access_token, api_version = api_version, offset = i)
    print(i)
    r_wall = requests.get(url_formatted)
    for post in r_wall.json()["response"]['items']:
        texts.append(post["text"])

with open("texts.txt", "wt", encoding = "utf8") as f:
    for text in texts:
        f.write(text.replace("\n", " ") + "\n")

# есть неточность в коде при формировании файла с постами. пока хз почему

# r_coms = requests.get(f'https://api.vk.com/method/wall.getComments?domain=nskgallery&count={numb}&access_token={access_token}&v={api_version}')
# url_coms = 'https://api.vk.com/method/wall.get?domain=nskgallery&count=4&offset={offset}&access_token={access_token}&v={api_version}'

# смотрим работу с CSV

# добавлена библ. mysqlclient