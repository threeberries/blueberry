# Main Application
# - Run it command line.
#
#
# @auth Steve (steve@lemoncloud.io)
#
import argparse
import pprint
from time import sleep

'''
------------------------------------------------------------------------------------
-- Main Application.
   자세한 실행 모드는 아래 각 함수 참고...
------------------------------------------------------------------------------------
'''
def main(param = None):
    _inf("hello main()....")
    parser = argparse.ArgumentParser()
    # running arguments...
    parser.add_argument('-m', '--mode', help='run mode (실행 모드)', default='')
    parser.add_argument('-i', '--item', help='item id (분석할 상품 MID)', default='5640996976')  # 진라면 순한맛
    parser.add_argument('-p', '--page', help='page (시작할 페이지 번호)', type=int, default=1)
    args = vars(parser.parse_args())
    
    # get parameters.
    mode = args['mode']
    page = args['page'] if 'page' in args else 1
    item = args['item'] if 'item' in args else ''
    items = [(('NS' if not x.startswith('NS') else '') + x) for x in item.split(',')]
    item = ('NS' if not item.startswith('NS') else '') + item
    _log('> items =', items)

    # mode = mode if mode else 'down-mid'
    # mode = mode if mode else 'auto-sync'
    mode = mode if mode else 'sync-deep'
    _log('! mode =', mode) if mode else ''

    # decode mode.
    ret = None
    if mode == 'pools':
        ret = run_mode_pools()
    elif mode == 'down-mid':
        ret = run_mode_down_mid()
    elif mode == 'auto-sync':
        ret = run_mode_auto_sync(page)
    elif mode == 'sync-deep':
        if len(items) <= 1:
            ret = run_mode_sync_list_deep(item, page, detail=True)
        else:
            ret = [run_mode_sync_list_deep(item, page, detail=True) for item in items ]
    else:
        _err('! unknown mode =', mode)
        ret = parser.print_help()
    
    #! print finally.
    _inf('! ret =', ret) if ret else ''


#---------------------------------------------
# mode: pools - test pools API
def run_mode_pools():
    from tools import pools
    pools.test()
    # eof - run_mode_pools
    return 0

#---------------------------------------------
# mode: down-mid - download
def run_mode_down_mid(mid = 'NS5640996976'):
    _inf('run_mode_down_mid(%s)...'%(mid))
    from tools import pools, tsv
    HEADERS = ['id','name','cat','price','delivery','mall','img']
    item = pools.describe_item(mid)
    # print('> item=', item)

    lines = []
    lines.append(HEADERS)
    lines.append([item.get(k, '') for k in HEADERS])
    # lines.append([(lambda k: item[k] if k in item else '')(k) for k in HEADERS])
    tsv.save_list_to_tsv(mid, lines)

    # load back.
    lines = tsv.load_list_from_tsv(mid)
    pprint.pprint(lines)

    # eof - run_mode_down_mid
    return 0

#---------------------------------------------
# mode: auto-sync - list items, then populate
def run_mode_auto_sync(page = None, total = None):
    page = 1 if page == None else page
    total = 0 if total == None else total
    _log('-----------------------------------------')
    _inf('run_mode_auto_sync(%d/%d)...'%(page, total))
    from tools import pools
    thiz = pools.get_items(page, 'ITEM')
    # print('> thiz=', thiz)
    
    # page = thiz['page']
    list = thiz['list']
    size = len(list)
    _log('> page=%d, size=%d'%(page, size))
    total += size

    #! do main task for each list.
    for node in list:
        item_id = node['id']
        name = node['name'] if 'name' in node else ''
        option = node['option'] if 'option' in node else None
        hasOption = True if option else False
        _log('>> id=', item_id, hasOption, ' - ', name)
        if not hasOption:
            res = run_mode_sync_list_deep(item_id, 1)
            _log('>>> res=', res)
            # exit()

    #! do next page.
    if size > 0 and page < 1000:
        sleep(0.5)
        return run_mode_auto_sync(page + 1, total)

    #! return total count.
    return {"total": total, "page": thiz['page']}


#---------------------------------------------
# mode: sync-list - call `sync-list` by page.
def run_mode_sync_list(item_id, page = None, total = None):
    page = 1 if page == None else page
    total = 0 if total == None else total
    _log('run_mode_sync_list(%s, %d/%d)...'%(item_id, page, total))
    from tools import pools
    thiz = pools.sync_list_item(item_id, page)
    # page = thiz['page']
    list = thiz['list'] if 'list' in thiz else []
    size = len(list)
    _log('> page=%d, size=%d'%(page, size))
    total += size
    #! return
    return {"total": total, "page": thiz['page'], "size": size, "list": list}

#---------------------------------------------
# mode: sync-deep - call `sync-list` in deep until eof
def run_mode_sync_list_deep(item_id, page = 1, total = 0, detail = False):
    from tools import pools
    _log('run_mode_sync_list_deep(%s, %d/%d)...'%(item_id, page, total))
    # do until EOF.
    for i in range(page, 200):            # max - 200 page
        res = run_mode_sync_list(item_id, i, total)
        list = res['list']
        total = res['total']
        size = res['size']

        # for detailed info for each malls.
        if (detail):
            _log('-- detailed[%02d:%02d].size = %d'%(page, i, size))
            for j, mall in enumerate(list):
                sleep(2)
                mid = mall['id']
                res2 = pools.sync_pull_item(mid)
                #TODO - APiError 404.
                _log('> [%03d:%02d:%02d] sync[%s] ='%(page, i, j, mid), res2)

        # check eof.
        if (size < 20):
            page = i
            break
        
    #! return
    return {"total": total, "page": page, "size": 0}


#---------------------------------------------
# print message with timestamp + color.
def _ts():
    import datetime
    now = datetime.datetime.now()
    return now.strftime('%Y-%m-%d %H:%M:%S')

def _log(*argv):
    print('\033[33m' + _ts() +'\033[0m', *argv)

def _inf(*argv):
    print('\033[32m' + _ts(), *argv, '\033[0m')

def _err(*argv):
    print('\033[31m' + _ts(), *argv, '\033[0m')


#############################
# Self Test Main.
if __name__ == '__main__':
    main()
