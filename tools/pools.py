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
#  - 검색을 시전함.
def get_items(page = None, type = None):
    param = {'ns':'NS', 'invalid':0}
    if (type != None): param['type'] = type
    if (page != None): param['page'] = page
    res = requests.get(_url('/item-pools/'), param)
    if res.status_code != 200:
        raise ApiError('Get Lists Error: {}'.format(res.status_code))
    return res.json()

#! get detail of item
#  - 상세 정보를 얻어옴.
def describe_item(item_id):
    res = requests.get(_url('/item-pools/{:s}/'.format(item_id)))
    if res.status_code != 200:
        raise ApiError('Get Item: {}'.format(res.status_code))
    return res.json()

#! call sync-list for item-id (ex: NS8159761521)
#  - ITEM 에 하위 MALL의 목록을 가져옴.
def sync_list_item(item_id, page = 1):
    res = requests.get(_url('/item-pools/{:s}/sync-list?page={:d}'.format(item_id, page)))
    if res.status_code != 200:
        raise ApiError('Get Item: {}'.format(res.status_code))
    return res.json()

#! call sync-pull for item-id (ex: NS8159761521)
#  - 각 MALL 에 대한 상세 정보 (이미지 포함)을 업데이트함.
def sync_pull_item(item_id):
    res = requests.get(_url('/item-pools/{:s}/sync-pull'.format(item_id)))
    if res.status_code != 200:
        raise ApiError('Get Item: {}'.format(res.status_code))
    return res.json()

#! update fields.
#  - 내부 속성을 업데이트 함.
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
