import pyxdf
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, timedelta
import time

data, header = pyxdf.load_xdf('BioSignalsPython_NOT_FOR_USE\dual_channel_data.xdf')



for stream in data:
    time_stamps = stream["time_stamps"]
    time_series = stream["time_series"]

    y = stream['time_series']

    #for timestamp, marker in zip(stream['time_stamps'], y):
        #print(f'Marker "{marker[0]}" @ {timestamp:.2f}s')

    timez = time_stamps
    what = time_series[ :,0]
    eda = time_series[ :,1]
    bvp = time_series[ :,2]
    
    plt.plot(what, bvp)
    print(len(bvp))
    


plt.show()