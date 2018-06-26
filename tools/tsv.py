"""
tsv.py
~~~~~~~~~~~~

Save/Read to 'data/XXXX.tsv' file.

:copyright: (c) 2018 by Steve (steve@lemoncloud.io)
:license: see LICENSE for more details.
"""
import pprint

# base of data folder
DATA_BASE = 'data/'
FILE_EXT = '.tsv'

# save lines to tsv 
#TODO - if type of lines is numpy, then use other-way.
def save_list_to_tsv(mid, lines = []):
    # import pandas as pd
    # import numpy as np
    import csv
    fname = DATA_BASE + mid + FILE_EXT
    print('> file.save =', fname)
    # pprint.pprint(lines)
    print('> lines.len =', len(lines))
    # np.savetxt(fname, lines, fmt='%s', delimiter='\t')
    with open(fname, 'w', encoding='utf-8') as f:
        wr = csv.writer(f, delimiter='\t')
        wr.writerows(lines)

# load lines from tsv
def load_list_from_tsv(mid):
    # import pandas as pd
    # import numpy as np
    import csv
    fname = DATA_BASE + mid + FILE_EXT
    print('> file.read =', fname)
    # lines = np.loadtxt(fname, delimiter='\t')
    # lines = pd.read_csv(fname, sep='\t')
    lines = []
    with open(fname, 'r', encoding='utf-8') as f:
        rdr = csv.reader(f, delimiter='\t')
        lines = list(rdr)
    print('> lines.len =', len(lines))
    return lines
