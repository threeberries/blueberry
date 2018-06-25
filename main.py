# Main Application
# - Run it command line.
#
# @auth Steve (steve@lemoncloud.io)
#
import argparse

'''
------------------------------------------------------------------------------------
-- Main Application.
------------------------------------------------------------------------------------
'''
def main(param = None):
    print("hello main()....")
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--mode', help='run mode (실행 모드)', default='')
    args = vars(parser.parse_args())
    mode = args['mode']
    
    # decode mode.
    if mode == 'pools':
        run_mode_pools()
    else:
        parser.print_help()


# mode: pools - test pools API
def run_mode_pools():
    from tools import pools
    pools.test()

#############################
# Self Test Main.
if __name__ == '__main__':
    main()
