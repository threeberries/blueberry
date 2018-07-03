# Main Application
# - Run it command line.
#
# @auth Steve (steve@lemoncloud.io)
#
import argparse
import pprint
from time import sleep

'''
------------------------------------------------------------------------------------
-- Main Application.
------------------------------------------------------------------------------------
'''
def main(param = None):
    print("hello main()....")
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--mode', help='run mode(실행 모드: pools)', default='')
    args = vars(parser.parse_args())
    mode = args['mode']
    # mode = mode if mode else 'down-mid'
    mode = mode if mode else 'auto-sync'
    print('! mode =', mode)

    # decode mode.
    ret = None
    if mode == 'pools':
        ret = run_mode_pools()
    elif mode == 'down-mid':
        ret = run_mode_down_mid()
    elif mode == 'auto-sync':
        ret = run_mode_auto_sync()
    else:
        ret = parser.print_help()
    
    #! print finally.
    print('! ret =', ret);


# mode: pools - test pools API
def run_mode_pools():
    from tools import pools
    pools.test()
    # eof - run_mode_pools
    return 0

# mode: down-mid - download
def run_mode_down_mid(mid = 'NS5640996976'):
    print('run_mode_down_mid(%s)...'%(mid))
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

# mode: auto-sync - list items, then populate
def run_mode_auto_sync(page = None, total = None):
    page = 1 if page == None else page
    total = 0 if total == None else total
    print('run_mode_auto_sync(%d/%d)...'%(page, total))
    from tools import pools
    thiz = pools.get_items(page, 'ITEM')
    # print('> thiz=', thiz)
    
    # page = thiz['page']
    list = thiz['list']
    size = len(list)
    print('> page=%d, size=%d'%(page, size))
    total += size

    #! do main task for each list.
    for node in list:
        item_id = node['id']
        name = node['name'] if 'name' in node else ''
        option = node['option'] if 'option' in node else None
        hasOption = True if option else False
        print('>> id=', item_id, hasOption, ' - ', name)
        if not hasOption:
            res = run_mode_sync_list_deep(item_id, 1)
            print('>>> res=', res)
            exit()

    #! do next page.
    if size > 0 and page < 100:
        sleep(0.5)
        return run_mode_auto_sync(page + 1, total)

    #! return total count.
    return {"total": total, "page": thiz['page']}


# mode: sync-list - call `sync-list` by page.
def run_mode_sync_list(item_id, page = None, total = None):
    page = 1 if page == None else page
    total = 0 if total == None else total
    print('run_mode_sync_list(%s, %d/%d)...'%(item_id, page, total))
    from tools import pools
    thiz = pools.sync_list_item(item_id, page)
    # page = thiz['page']
    list = thiz['list'] if 'list' in thiz else []
    size = len(list)
    print('> page=%d, size=%d'%(page, size))
    total += size
    #! return
    return {"total": total, "page": thiz['page'], "size": size, "list": list}

# mode: sync-list-deep - call `sync-list` in deep until eof
def run_mode_sync_list_deep(item_id, page = 1, total = 0):
    from tools import pools
    print('run_mode_sync_list_deep(%s, %d/%d)...'%(item_id, page, total))
    for i in range(page, 100):            # max - 100 page
        res = run_mode_sync_list(item_id, i, total)
        list = res['list']
        total = res['total']
        size = res['size']

        # for each mall. call sync-pull.
        for i, mall in enumerate(list):
            sleep(2)
            mid = mall['id']
            res2 = pools.sync_pull_item(mid)
            print('%03d:%02d> sync[%s] ='%(page, i, mid), res2)

        # check eof.
        if (size < 20):
            page = i
            break
        
    #! return
    return {"total": total, "page": page, "size": 0}


#############################
# Self Test Main.
if __name__ == '__main__':
    main()
