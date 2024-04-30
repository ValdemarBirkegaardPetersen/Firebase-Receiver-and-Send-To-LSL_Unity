import pyxdf
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, timedelta
import time
import heartpy as hp


data, header = pyxdf.load_xdf('test2.xdf')



# Used for getting markers
marker_stream = data[0]
marker_time_stamps = marker_stream["time_stamps"]
marker_time_series = marker_stream["time_series"]

print(marker_time_series)


# Used for getting actual data
data_stream = data[1]
time_stamps = data_stream["time_stamps"]
time_series = data_stream["time_series"]
    
timer = time_stamps
what = time_series[ :,0]
bvp = time_series[ :,1]
eda = time_series[ :,2]

print(eda)


