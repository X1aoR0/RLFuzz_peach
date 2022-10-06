import os
import numpy as np
import matplotlib as mpl

mpl.use('Agg')

import scipyplot as spp
import matplotlib.pyplot as plt

#
files = os.listdir('.')
for each in files:
    if each.endswith('.npy'):
        data_json = np.load(os.path.join(os.getcwd(), each), allow_pickle=True)
        data = data_json.item()
        # h = spp.rplot(np.array(data['unique_path_history']))
        # spp.save2file('test',h)
        print(1)