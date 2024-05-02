import pyxdf
import numpy as np
from datetime import datetime, timedelta
import time
import heartpy as hp
from scipy.signal import find_peaks
import neurokit2 as nk

import matplotlib.pyplot as plt

data, header = pyxdf.load_xdf('test6.xdf')


def get_marker_time_series(data):
    marker_stream = data[0]
    marker_time_stamps = marker_stream["time_stamps"]
    marker_time_series = marker_stream["time_series"]

    marker_dict = {}
    for x in range(len(marker_time_stamps)):
        marker_dict[marker_time_stamps[x]] = marker_time_series[x]
        
    print(marker_dict)
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


def plot_eda_with_peaks(data_timestamps, eda):
    # Normalize EDA data if needed (depending on the range and scale)
    eda = (eda - np.min(eda)) / (np.max(eda) - np.min(eda))

    # Find peaks which might correspond to SCRs
    peaks, _ = find_peaks(eda, height=0.1)  # height threshold is adjustable based on your data characteristics

    # Plot EDA data and mark peaks
    plt.figure(figsize=(12, 6))
    plt.plot(data_timestamps, eda, label='EDA')
    plt.scatter(data_timestamps[peaks], eda[peaks], color='red', label='Peaks')  # mark peaks
    plt.title('EDA Signal with Detected Peaks')
    plt.xlabel('Time (s)')
    plt.ylabel('Normalized EDA')
    plt.legend()
    plt.show()
    


marker_timestamps, marker_timeseries = get_marker_time_series(data)

data_timestamps, huh, bvp, eda = get_bvp_and_eda_data(data)

analyze_bvp_data(bvp)
#plot_eda_with_peaks(data_timestamps,eda)



def analyze_eda_data(eda, sampling_rate):
# SDNN:
# Normal: 50-100 ms
# High: >100 ms
# Low: <50 ms

# RMSSD:
# Normal: 20-50 ms (typical for healthy adults)
# High: >50 ms (common in young, healthy, or well-trained individuals)
# Low: <20 ms (may indicate stress or health issues)

    signals, info = nk.eda_process(eda, sampling_rate=sampling_rate)
    analyze_df = nk.eda_analyze(signals, sampling_rate=sampling_rate)
    mean_eda = np.mean(eda)
    return analyze_df, mean_eda

analyze_df, mean_eda = analyze_eda_data(eda, sampling_rate=1000)
print(analyze_df)
print("Mean EDA:", mean_eda)

eda_signals, info = nk.eda_process(eda, sampling_rate=1000)

nk.eda_plot(eda_signals, info)