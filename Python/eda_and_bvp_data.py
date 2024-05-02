import pyxdf
import numpy as np
from datetime import datetime, timedelta
import time
import heartpy as hp
from scipy.signal import find_peaks
import neurokit2 as nk

import matplotlib.pyplot as plt

data, header = pyxdf.load_xdf('test6.xdf')

# CURERNT CHATGPT PROMPT # 
'''
I have a 1D array called 'bvp' that contains raw blood volume pulse values. I have another 1d array with the same excact length, that contains each bvp values corresponding timestamps. 

I then have two 1d arrays, that are called "marker_timestamps" which contains the time for when the marker was placed,  and "marker_timeseries" which contains the value/name of the marker such as "Task 1 Started". After a task is started, it will always be followed by a next marker which inditates when task ended, this marker will always be named "Task Finished" and will occurence after the "Task X Started". This is how the bvp data should be segmented, from that Started timestamp to the Task Finished timestamps. I have 5 events, so there should be five segmentations
'''

def get_marker_time_series(data):
    marker_stream = data[0]
    marker_time_stamps = marker_stream["time_stamps"]
    marker_time_series = marker_stream["time_series"]

    marker_dict = {}
    for x in range(len(marker_time_stamps)):
        marker_dict[marker_time_stamps[x]] = marker_time_series[x]
        
    return marker_time_stamps, marker_time_series


def get_bvp_and_eda_data(data):
    
    data_stream = data[1]
    data_timestamps = data_stream["time_stamps"]
    data_timeseries = data_stream["time_series"]
    
    huh = data_timeseries[ :,0]
    bvp = data_timeseries[ :,1]
    eda = data_timeseries[ :,2]
    
    return data_timestamps, huh, bvp, eda

def get_bvp_and_eda_data_for_bugged_data(data):
    data_stream = data[0]
    data_timestamps = data_stream["time_stamps"]
    data_timeseries = data_stream["time_series"]
    
    huh = data_timeseries[ :,0]
    bvp = data_timeseries[ :,1]
    eda = data_timeseries[ :,2]
    
    return data_timestamps, huh, bvp, eda


def analyze_bvp_single_data(bvp):
    sampling_rate = 1000
    processed_data, measures = hp.process(bvp, sampling_rate)
    
    print("Heart Rate Measures:")
    print("BPM:", measures['bpm'])
    print("IBI:", measures['ibi'])
    print("SDNN:", measures['sdnn'])
    print("RMSSD:", measures['rmssd'])
    
def analyze_bvp_baseline_data(bvp_baseline):
    sampling_rate = 1000
    processed_data, measures = hp.process(bvp_baseline, sampling_rate)
    
    print("\n---------------------------------------------------------------------------------")
    print("Baseline")
    print("Heart Rate Measures:")
    print("BPM:", measures['bpm'])
    print("IBI:", measures['ibi'])
    print("SDNN:", measures['sdnn'])
    print("RMSSD:", measures['rmssd'])

def analyze_bvp_task_data(bvp1, bvp2, bvp3, bvp4, bvp5, sampling_rate=1000):
    processed_data, measures = hp.process(bvp1, sampling_rate)
    print("\n---------------------------------------------------------------------------------")
    print("Task 1 \n")
    print("Heart Rate Measures:")
    print("BPM:", measures['bpm'])
    print("IBI:", measures['ibi'])
    print("SDNN:", measures['sdnn'])
    print("RMSSD:", measures['rmssd'])
    
    processed_data, measures = hp.process(bvp2, sampling_rate)
    print("\n---------------------------------------------------------------------------------")
    print("Task 2 \n")
    print("Heart Rate Measures:")
    print("BPM:", measures['bpm'])
    print("IBI:", measures['ibi'])
    print("SDNN:", measures['sdnn'])
    print("RMSSD:", measures['rmssd'])
    
    processed_data, measures = hp.process(bvp4, sampling_rate)
    print("\n---------------------------------------------------------------------------------")
    print("Task 3 \n")
    print("Heart Rate Measures:")
    print("BPM:", measures['bpm'])
    print("IBI:", measures['ibi'])
    print("SDNN:", measures['sdnn'])
    print("RMSSD:", measures['rmssd'])
    
    processed_data, measures = hp.process(bvp5, sampling_rate)
    print("\n---------------------------------------------------------------------------------")
    print("Task 4 \n")
    print("Heart Rate Measures:")
    print("BPM:", measures['bpm'])
    print("IBI:", measures['ibi'])
    print("SDNN:", measures['sdnn'])
    print("RMSSD:", measures['rmssd'])
    
    processed_data, measures = hp.process(bvp1, sampling_rate)
    print("\n---------------------------------------------------------------------------------")
    print("Task 5 \n")
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
    

def analyze_eda_single_data(eda, sampling_rate):
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

def analyze_eda_baseline_data(eda_baseline, sampling_rate=1000):
# SDNN:
# Normal: 50-100 ms
# High: >100 ms
# Low: <50 ms

# RMSSD:
# Normal: 20-50 ms (typical for healthy adults)
# High: >50 ms (common in young, healthy, or well-trained individuals)
# Low: <20 ms (may indicate stress or health issues)

    print("\n---------------------------------------------------------------------------------")
    print("Baseline")
    signals, info = nk.eda_process(eda_baseline, sampling_rate=sampling_rate)
    analyze_df = nk.eda_analyze(signals, sampling_rate=sampling_rate)
    mean_eda = np.mean(eda_baseline)
    print(analyze_df) 
    print("EDA Mean:  " + str(mean_eda))

def analyze_eda_task_data(eda_task1, eda_task2, eda_task3, eda_task4, eda_task5, sampling_rate):
    print("\n---------------------------------------------------------------------------------")
    print("Task 1 \n")
    signals, info = nk.eda_process(eda_task1, sampling_rate=sampling_rate)
    analyze_df = nk.eda_analyze(signals, sampling_rate=sampling_rate)
    mean_eda = np.mean(eda_task1)
    print(analyze_df) 
    print("EDA Mean:  " + str(mean_eda))
    
    print("---------------------------------------------------------------------------------")
    print("Task 2 \n")
    signals, info = nk.eda_process(eda_task2, sampling_rate=sampling_rate)
    analyze_df = nk.eda_analyze(signals, sampling_rate=sampling_rate)
    mean_eda = np.mean(eda_task2)
    print(analyze_df) 
    print("EDA Mean:  " + str(mean_eda))
    
    print("---------------------------------------------------------------------------------")
    print("Task 3 \n")
    signals, info = nk.eda_process(eda_task3, sampling_rate=sampling_rate)
    analyze_df = nk.eda_analyze(signals, sampling_rate=sampling_rate)
    mean_eda = np.mean(eda_task3)
    print(analyze_df) 
    print("EDA Mean:  " + str(mean_eda))
    
    print("---------------------------------------------------------------------------------")
    print("Task 4 \n")
    signals, info = nk.eda_process(eda_task4, sampling_rate=sampling_rate)
    analyze_df = nk.eda_analyze(signals, sampling_rate=sampling_rate)
    mean_eda = np.mean(eda_task4)
    print(analyze_df) 
    print("EDA Mean:  " + str(mean_eda))
    
    print("---------------------------------------------------------------------------------")
    print("Task 5 \n")
    signals, info = nk.eda_process(eda_task5, sampling_rate=sampling_rate)
    analyze_df = nk.eda_analyze(signals, sampling_rate=sampling_rate)
    mean_eda = np.mean(eda_task5)
    print(analyze_df) 
    print("EDA Mean:  " + str(mean_eda))
    

def extract_task_segments(marker_timestamps, marker_timeseries, data_timestamps, dataz):
    segments = []
    for i, marker in enumerate(marker_timeseries):
        if "Started" in marker[0]:
            start_time = marker_timestamps[i]
            end_time = marker_timestamps[i + 1]  # Assumes the next marker is the end
            start_index = np.searchsorted(data_timestamps, start_time)
            end_index = np.searchsorted(data_timestamps, end_time)
            segment = dataz[start_index:end_index]
            segments.append((start_time, end_time, segment))
        
    task1_data = segments[0][2]
    task2_data = segments[1][2]
    task3_data = segments[2][2]
    task4_data = segments[3][2] 
    task5_data = segments[4][2]
    
    return task1_data, task2_data, task3_data, task4_data, task5_data
    


def main():
    

    marker_timestamps, marker_timeseries = get_marker_time_series(data)

    data_timestamps, huh, bvp, eda = get_bvp_and_eda_data(data)
    #data_timestamps, huh, bvp, eda = get_bvp_and_eda_data_for_bugged_data(data)

    # BVP
    #analyze_bvp_data(bvp)


    analyze_bvp_baseline_data(bvp)
    analyze_eda_baseline_data(eda)

    #task1_bvp, task2_bvp, task3_bvp, task4_bvp, task5_bvp = extract_task_segments(marker_timestamps, marker_timeseries, data_timestamps, bvp)
    #task1_eda, task2_eda, task3_eda, task4_eda, task5_eda = extract_task_segments(marker_timestamps, marker_timeseries, data_timestamps, eda)
    
    #analyze_eda_task_data(task1_eda, task2_eda, task3_eda, task4_eda, task5_eda, sampling_rate=1000)
    #analyze_bvp_task_data(task1_bvp, task2_bvp, task3_bvp, task4_bvp, task5_bvp, sampling_rate=1000)


if __name__ == "__main__":
    main()