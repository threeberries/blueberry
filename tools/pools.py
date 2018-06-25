"""
pools.api
~~~~~~~~~~~~

Requests API for `item-pools` Service.

:copyright: (c) 2018 by Steve (steve@lemoncloud.io)
:license: MIT, see LICENSE for more details.
"""

#! install requests if required!.
# $ pip install requests
import requests

#! 8084는 `item-pools`의 API 주소로, 로컬 환경 개발시 터널링을 이용함.
BASE_URL   = 'http://localhost:8084'

#! class ApiError
class ApiError(BaseException):
    def __init__(self, msg):
        self.message = msg

#! get target url
def _url(path):
    return BASE_URL + path

#! get items : {list, page, total}
def get_items():
    res = requests.get(_url('/item-pools/'), {'ns':'NS'})
    if res.status_code != 200:
        raise ApiError('Get Lists Error: {}'.format(res.status_code))
    return res.json()

#! get detail of item
def describe_item(item_id):
    res = requests.get(_url('/item-pools/{:s}/'.format(item_id)))
    if res.status_code != 200:
        raise ApiError('Get Item: {}'.format(res.status_code))
    return res.json()

#! update fields.
def update_item(item_id, description):
    url = _url('/item-pools/{:s}/'.format(item_id))
    res = requests.put(url, json= {'description': description})
    if res.status_code != 200:
        raise ApiError('Update Item: {}'.format(res.status_code))
    return res.json()

def test():
    print('-- %s'%('/item-pools/{:s}/'.format('abcd')))
    data = get_items()
    print('> total=',   data['total'])
    print('> page=',    data['page'])
    item = describe_item(data['list'][0]['id'])
    print('> items[0].id =',    item['id'])
    print('> items[0].type =',  item['type'])
    print('> items[0].name =',  item['name'])
