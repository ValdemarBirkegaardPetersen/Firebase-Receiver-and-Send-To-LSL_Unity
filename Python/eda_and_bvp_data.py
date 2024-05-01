import pyxdf
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, timedelta
import time
import heartpy as hp


data, header = pyxdf.load_xdf('test5.xdf')



def get_marker_time_series(data):
    marker_stream = data[0]
    marker_time_stamps = marker_stream["time_stamps"]
    marker_time_series = marker_stream["time_series"]
    return marker_time_stamps, marker_time_series


def get_bvp_and_eda_data(data):
    data_stream = data[1]
    data_timestamps = data_stream["time_stamps"]
    data_timeseries = data_stream["time_series"]
    
    huh = data_timeseries[ :,0]
    bvp = data_timeseries[ :,1]
    eda = data_timeseries[ :,2]
    
    return data_timestamps, huh, bvp, eda

def analyze_bvp_data(bvp):
    sampling_rate = 1000
    processed_data, measures = hp.process(bvp, sampling_rate)
    
    print("Heart Rate Measures:")
    print("BPM:", measures['bpm'])
    print("IBI:", measures['ibi'])
    print("SDNN:", measures['sdnn'])
    print("RMSSD:", measures['rmssd'])



marker_timestamps, marker_timeseries = get_marker_time_series(data)

data_timestamps, huh, bvp, eda = get_bvp_and_eda_data(data)

# Call the function with the bvp data and sampling rate
analyze_bvp_data(bvp)



