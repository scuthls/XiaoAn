
import requests

import json

api = "6b2db33d931048ccb876a491f334c4f6"

url = 'http://www.tuling123.com/openapi/api?key=' + api + '&info='

while 1:
    info = input("用户：")
    page = requests.get(url + info)
    json_dic = json.loads(page.text)
    answer = json_dic['text']
    print('小安: ',answer)
