import pyxdf
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, timedelta
import time
import csv
import os
print(os.getcwd())


def save_to_csv(timestamps, markers, filename='output.csv'):
    filepath = os.path.join(os.getcwd(), filename)
    with open(filepath, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['timestamp', 'marker'])
        writer.writerows(zip(timestamps, markers))
    print(f"File saved at: {filepath}")


data, header = pyxdf.load_xdf("sub-P003_ses-S001_task-Default_run-001_eeg.xdf")

for stream in data:
    time_stamps = stream["time_stamps"]
    markers = stream["time_series"]

    print(len(time_stamps))
    print(len(markers))
    
    #save_to_csv(time_stamps, markers, filename='P001.csv')
    
    




