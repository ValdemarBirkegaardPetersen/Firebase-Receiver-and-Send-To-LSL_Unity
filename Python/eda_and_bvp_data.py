import json
import requests
import pyxdf
import numpy as np
from datetime import datetime, timedelta
import time
import heartpy as hp
from scipy.signal import find_peaks
import neurokit2 as nk

import matplotlib.pyplot as plt

data, header = pyxdf.load_xdf("test6.xdf")

# CURERNT CHATGPT PROMPT #
"""
I have a 1D array called 'bvp' that contains raw blood volume pulse values. I have another 1d array with the same excact length, that contains each bvp values corresponding timestamps. 

I then have two 1d arrays, that are called "marker_timestamps" which contains the time for when the marker was placed,  and "marker_timeseries" which contains the value/name of the marker such as "Task 1 Started". After a task is started, it will always be followed by a next marker which inditates when task ended, this marker will always be named "Task Finished" and will occurence after the "Task X Started". This is how the bvp data should be segmented, from that Started timestamp to the Task Finished timestamps. I have 5 events, so there should be five segmentations
"""


def get_marker_time_series(data):
    marker_stream = data[0]
    marker_time_stamps = marker_stream["time_stamps"]
    marker_time_series = marker_stream["time_series"]

    print(marker_time_series)

    marker_dict = {}
    for x in range(len(marker_time_stamps)):
        marker_dict[marker_time_stamps[x]] = marker_time_series[x]

    return marker_time_stamps, marker_time_series


def get_bvp_and_eda_data(data):

    data_stream = data[1]
    print(data_stream)
    data_timestamps = data_stream["time_stamps"]
    data_timeseries = data_stream["time_series"]

    print(data_timeseries)
    huh = data_timeseries[:, 0]
    bvp = data_timeseries[:, 1]
    eda = data_timeseries[:, 2]

    return data_timestamps, huh, bvp, eda


def get_bvp_and_eda_data_for_bugged_data(data):
    data_stream = data[0]
    data_timestamps = data_stream["time_stamps"]
    data_timeseries = data_stream["time_series"]

    huh = data_timeseries[:, 0]
    bvp = data_timeseries[:, 1]
    eda = data_timeseries[:, 2]

    return data_timestamps, huh, bvp, eda


def analyze_bvp_single_data(bvp):
    sampling_rate = 1000
    processed_data, measures = hp.process(bvp, sampling_rate)

    print("Heart Rate Measures:")
    print("BPM:", measures["bpm"])
    print("IBI:", measures["ibi"])
    print("SDNN:", measures["sdnn"])
    print("RMSSD:", measures["rmssd"])


def analyze_bvp_baseline_data(bvp_baseline):
    sampling_rate = 1000
    processed_data, measures = hp.process(bvp_baseline, sampling_rate)

    print(
        "\n---------------------------------------------------------------------------------"
    )
    print("Baseline")
    print("Heart Rate Measures:")
    print("BPM:", measures["bpm"])
    print("IBI:", measures["ibi"])
    print("SDNN:", measures["sdnn"])
    print("RMSSD:", measures["rmssd"])


def analyze_bvp_task_data(bvp1, bvp2, bvp3, bvp4, bvp5, sampling_rate=1000):
    task1_bmp = None
    task1_sdnn = None
    task1_rmssd = None

    task2_bmp = None
    task2_sdnn = None
    task2_rmssd = None

    task3_bmp = None
    task3_sdnn = None
    task3_rmssd = None

    task4_bmp = None
    task4_sdnn = None
    task4_rmssd = None

    task5_bmp = None
    task5_sdnn = None
    task5_rmssd = None

    print(
        "\n---------------------------------------------------------------------------------"
    )
    print("Task 1 \n")
    #bvp1 = hp.enhance_peaks(bvp1)
    processed_data, measures = hp.process(bvp1, sampling_rate)
    print("Heart Rate Measures:")
    print("BPM:", measures["bpm"])
    task1_bmp = measures["bpm"]
    print("IBI:", measures["ibi"])
    print("SDNN:", measures["sdnn"])
    task1_sdnn = measures["sdnn"]
    print("RMSSD:", measures["rmssd"])
    task1_rmssd = measures["rmssd"]

    print(
        "\n---------------------------------------------------------------------------------"
    )
    print("Task 2 \n")
    #bvp2 = hp.enhance_peaks(bvp2)
    processed_data, measures = hp.process(bvp2, sampling_rate)
    print("Heart Rate Measures:")
    print("BPM:", measures["bpm"])
    task2_bmp = measures["bpm"]
    print("IBI:", measures["ibi"])
    print("SDNN:", measures["sdnn"])
    task2_sdnn = measures["sdnn"]
    print("RMSSD:", measures["rmssd"])
    task2_rmssd = measures["rmssd"]

    print(
        "\n---------------------------------------------------------------------------------"
    )
    print("Task 3 \n")
    #bvp3 = hp.enhance_peaks(bvp3)
    processed_data, measures = hp.process(bvp3, sampling_rate)
    print("Heart Rate Measures:")
    print("BPM:", measures["bpm"])
    task3_bmp = measures["bpm"]
    print("IBI:", measures["ibi"])
    print("SDNN:", measures["sdnn"])
    task3_sdnn = measures["sdnn"]
    print("RMSSD:", measures["rmssd"])
    task3_rmssd = measures["rmssd"]

    print(
        "\n---------------------------------------------------------------------------------"
    )
    print("Task 4 \n")
    #bvp4 = hp.enhance_peaks(bvp4)
    processed_data, measures = hp.process(bvp4, sampling_rate)
    print("Heart Rate Measures:")
    print("BPM:", measures["bpm"])
    task4_bmp = measures["bpm"]
    print("IBI:", measures["ibi"])
    print("SDNN:", measures["sdnn"])
    task4_sdnn = measures["sdnn"]
    print("RMSSD:", measures["rmssd"])
    task4_rmssd = measures["rmssd"]

    print(
        "\n---------------------------------------------------------------------------------"
    )
    print("Task 5 \n")
    #bvp5 = hp.enhance_peaks(bvp5)
    processed_data, measures = hp.process(bvp5, sampling_rate)
    print("Heart Rate Measures:")
    print("BPM:", measures["bpm"])
    task5_bmp = measures["bpm"]
    print("IBI:", measures["ibi"])
    print("SDNN:", measures["sdnn"])
    task5_sdnn = measures["sdnn"]
    print("RMSSD:", measures["rmssd"])
    task5_rmssd = measures["rmssd"]

    return task1_bmp, task1_sdnn, task1_rmssd, task2_bmp, task2_sdnn, task2_rmssd, task3_bmp, task3_sdnn, task3_rmssd, task4_bmp, task4_sdnn, task4_rmssd, task5_bmp, task5_sdnn, task5_rmssd


def plot_eda_with_peaks(data_timestamps, eda):
    # Normalize EDA data if needed (depending on the range and scale)
    eda = (eda - np.min(eda)) / (np.max(eda) - np.min(eda))

    # Find peaks which might correspond to SCRs
    peaks, _ = find_peaks(
        eda, height=0.1
    )  # height threshold is adjustable based on your data characteristics

    # Plot EDA data and mark peaks
    plt.figure(figsize=(12, 6))
    plt.plot(data_timestamps, eda, label="EDA")
    plt.scatter(
        data_timestamps[peaks], eda[peaks], color="red", label="Peaks"
    )  # mark peaks
    plt.title("EDA Signal with Detected Peaks")
    plt.xlabel("Time (s)")
    plt.ylabel("Normalized EDA")
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

    print(
        "\n---------------------------------------------------------------------------------"
    )
    print("Baseline")
    signals, info = nk.eda_process(eda_baseline, sampling_rate=sampling_rate)
    analyze_df = nk.eda_analyze(signals, sampling_rate=sampling_rate)
    mean_eda = np.mean(eda_baseline)
    print("EDA Mean:  " + str(mean_eda))
    print(analyze_df)


def analyze_eda_task_data(
    eda_task1, eda_task2, eda_task3, eda_task4, eda_task5, sampling_rate
):
    task1_src_n = None
    task1_src_amplitude_avg = None
    task1_eda_mean = None

    task2_src_n = None
    task2_src_amplitude_avg = None
    task2_eda_mean = None

    task3_src_n = None
    task3_src_amplitude_avg = None
    task3_eda_mean = None

    task4_src_n = None
    task4_src_amplitude_avg = None
    task4_eda_mean = None

    task5_src_n = None
    task5_src_amplitude_avg = None
    task5_eda_mean = None

    print(
        "\n---------------------------------------------------------------------------------"
    )
    print("Task 1 \n")
    signals, info = nk.eda_process(eda_task1, sampling_rate=sampling_rate)
    analyze_df = nk.eda_analyze(signals, sampling_rate=sampling_rate)
    task1_src_n = analyze_df["SCR_Peaks_N"]
    task1_src_amplitude_avg = analyze_df["SCR_Peaks_Amplitude_Mean"]
    task1_eda_mean = np.mean(eda_task1)
    print(analyze_df)
    print("EDA Mean:  " + str(task1_eda_mean))

    print(
        "---------------------------------------------------------------------------------"
    )
    print("Task 2 \n")
    signals, info = nk.eda_process(eda_task2, sampling_rate=sampling_rate)
    analyze_df = nk.eda_analyze(signals, sampling_rate=sampling_rate)
    task2_src_n = analyze_df["SCR_Peaks_N"]
    task2_src_amplitude_avg = analyze_df["SCR_Peaks_Amplitude_Mean"]
    task2_eda_mean = np.mean(eda_task2)
    print(analyze_df)
    print("EDA Mean:  " + str(task2_eda_mean))

    print(
        "---------------------------------------------------------------------------------"
    )
    print("Task 3 \n")
    signals, info = nk.eda_process(eda_task3, sampling_rate=sampling_rate)
    analyze_df = nk.eda_analyze(signals, sampling_rate=sampling_rate)
    task3_src_n = analyze_df["SCR_Peaks_N"]
    task3_src_amplitude_avg = analyze_df["SCR_Peaks_Amplitude_Mean"]
    task3_eda_mean = np.mean(eda_task3)
    print(analyze_df)
    print("EDA Mean:  " + str(task3_eda_mean))

    print(
        "---------------------------------------------------------------------------------"
    )
    print("Task 4 \n")
    signals, info = nk.eda_process(eda_task4, sampling_rate=sampling_rate)
    analyze_df = nk.eda_analyze(signals, sampling_rate=sampling_rate)
    task4_src_n = analyze_df["SCR_Peaks_N"]
    task4_src_amplitude_avg = analyze_df["SCR_Peaks_Amplitude_Mean"]
    task4_eda_mean = np.mean(eda_task4)
    print(analyze_df)
    print("EDA Mean:  " + str(task4_eda_mean))

    print(
        "---------------------------------------------------------------------------------"
    )
    print("Task 5 \n")
    signals, info = nk.eda_process(eda_task5, sampling_rate=sampling_rate)
    analyze_df = nk.eda_analyze(signals, sampling_rate=sampling_rate)
    task5_src_n = analyze_df["SCR_Peaks_N"]
    task5_src_amplitude_avg = analyze_df["SCR_Peaks_Amplitude_Mean"]
    task5_eda_mean = np.mean(eda_task5)
    print(analyze_df)
    print("EDA Mean:  " + str(task5_eda_mean))

    return (
        task1_src_n,
        task1_src_amplitude_avg,
        task1_eda_mean,
        task2_src_n,
        task2_src_amplitude_avg,
        task2_eda_mean,
        task3_src_n,
        task3_src_amplitude_avg,
        task3_eda_mean,
        task4_src_n,
        task4_src_amplitude_avg,
        task4_eda_mean,
        task5_src_n,
        task5_src_amplitude_avg,
        task5_eda_mean,
    )


def extract_task_segments(marker_timestamps, marker_timeseries, data_timestamps, dataz):
    segments = []
    for i, marker in enumerate(marker_timeseries):
        if "Started" in marker[0]:
            start_time = marker_timestamps[i]
            # Assumes the next marker is the end
            end_time = marker_timestamps[i + 1]
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


def post_task_data(t1_1, t1_2, t1_3, t2_1, t2_2, t2_3, t3_1, t3_2, t3_3, t4_1, t4_2, t4_3, t5_1, t5_2, t5_3):
    # Set up the URL and the API endpoint
    url = "https://sheetdb.io/api/v1/ptq705dc9tdgp"

    # Prepare headers
    headers = {"Accept": "application/json",
               "Content-Type": "application/json"}

    # Prepare data payload
    data = {
        "data": [
            {
                "Task 1 - BPM": float(t1_1),
                "Task 1 - SDNN": float(t1_2),
                "Task 1 - RMSSD": float(t1_3),
                "Task 2 - BPM": float(t2_1),
                "Task 2 - SDNN": float(t2_2),
                "Task 2 - RMSSD": float(t2_3),
                "Task 3 - BPM": float(t3_1),
                "Task 3 - SDNN": float(t3_2),
                "Task 3 - RMSSD": float(t3_3),
                "Task 4 - BPM": float(t4_1),
                "Task 4 - SDNN": float(t4_2),
                "Task 4 - RMSSD": float(t4_3),
                "Task 5 - BPM": float(t5_1),
                "Task 5 - SDNN": float(t5_2),
                "Task 5 - RMSSD": float(t5_3)
            }
        ]
    }

    # Make the POST request
    response = requests.post(url, headers=headers, data=json.dumps(data))

    # Convert the response to JSON
    response_json = response.json()

    # Print the result
    print(response_json)


def main():

    marker_timestamps, marker_timeseries = get_marker_time_series(data)

    data_timestamps, huh, bvp, eda = get_bvp_and_eda_data(data)
    # data_timestamps, huh, bvp, eda = get_bvp_and_eda_data_for_bugged_data(data)

    # BVP
    # analyze_bvp_data(bvp)
    
    #analyze_bvp_baseline_data(bvp)
    #analyze_eda_baseline_data(eda)
    

    task1_bvp, task2_bvp, task3_bvp, task4_bvp, task5_bvp = extract_task_segments(
        marker_timestamps, marker_timeseries, data_timestamps, bvp)

    task1_eda, task2_eda, task3_eda, task4_eda, task5_eda = extract_task_segments(
        marker_timestamps, marker_timeseries, data_timestamps, eda)

    task1_bmp, task1_sdnn, task1_rmssd, task2_bmp, task2_sdnn, task2_rmssd, task3_bmp, task3_sdnn, task3_rmssd, task4_bmp, task4_sdnn, task4_rmssd, task5_bmp, task5_sdnn, task5_rmssd = analyze_bvp_task_data(
        task1_bvp, task2_bvp, task3_bvp, task4_bvp, task5_bvp, sampling_rate=1000)
    
    print(task1_bmp)
    
    post_task_data(task1_bmp, task1_sdnn, task1_rmssd,
                   task2_bmp, task2_sdnn, task2_rmssd,
                   task3_bmp, task3_sdnn, task3_rmssd,
                   task4_bmp, task4_sdnn, task4_rmssd,
                   task5_bmp, task5_sdnn, task5_rmssd)

    (
        task1_src_n, task1_src_amplitude_avg, task1_eda_mean,
        task2_src_n, task2_src_amplitude_avg, task2_eda_mean,
        task3_src_n, task3_src_amplitude_avg, task3_eda_mean,
        task4_src_n, task4_src_amplitude_avg, task4_eda_mean,
        task5_src_n, task5_src_amplitude_avg, task5_eda_mean
    ) = analyze_eda_task_data(task1_eda, task2_eda, task3_eda, task4_eda, task5_eda, sampling_rate=1000)

    post_task_data(task1_src_n[0], task1_src_amplitude_avg[0], task1_eda_mean,
                   task2_src_n[0], task2_src_amplitude_avg[0], task2_eda_mean,
                   task3_src_n[0], task3_src_amplitude_avg[0], task3_eda_mean,
                   task4_src_n[0], task4_src_amplitude_avg[0], task4_eda_mean,
                   task5_src_n[0], task5_src_amplitude_avg[0], task5_eda_mean)
                   
    


if __name__ == "__main__":
    main()
