# Main Application
# - Run it command line.
#
# @auth Steve (steve@lemoncloud.io)
#
import argparse
import pprint

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
    mode = mode if mode else 'down-mid'
    print('! mode =', mode)

    # decode mode.
    if mode == 'pools':
        run_mode_pools()
    elif mode == 'down-mid':
        run_mode_down_mid()
    else:
        parser.print_help()


# mode: pools - test pools API
def run_mode_pools():
    from tools import pools
    pools.test()

# mode: down-mid - download
def run_mode_down_mid(mid = 'NS5640996976'):
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


#############################
# Self Test Main.
if __name__ == '__main__':
    main()
