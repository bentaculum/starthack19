import requests
import json

from csv_streaming import load_csvs, stream_to_csv
from config import config
from flask import Flask
import pandas as pd
import os
import glob
import numpy as np
import time
import csv
import threading

dataLock = threading.Lock()
# thread handler
yourThread = threading.Thread()

def create_app():
    global yourThread
    app = Flask(__name__)

    def run_on_start(*args, **argv):
        # absolut base_dir
        base_dir = config['base_dir']
        os.chdir(base_dir)
        golden_table = load_csvs(os.path.join(base_dir, config['car_subdir']),
                                 os.path.join(base_dir, config['watch_subdir']))
        print('shape of golden table: {}'.format(golden_table.shape))
        stream_to_csv(golden_table, os.path.join(base_dir, config['tmp_subdir']), config['stream_filename'])

    # run streaming in background thread, visible in global context
    yourThread = threading.Thread(target=run_on_start)
    yourThread.start()

    return app

app = create_app()


# url = "http://130.82.239.210"

@app.route("/driver")
def driver_ready():
    data = pd.read_csv(os.path.join(config['base_dir'],config['tmp_subdir'],config['stream_filename']))
    # print(data.shape)
    # print('cap {} rev {} speed {} hr {} sweatbleh {}'.format(has_capacity(data), calm_driving(data), smooth_speed(data), heart_rate_ok(data), no_sweating(data)))
    if has_capacity(data) and calm_driving(data) and smooth_speed(data) and heart_rate_ok(data) and no_sweating(data):
        return "True"
    else:
        return "False"


# HELPER FUNCTIONS BELOW

# determines whether the driver is not excessively sweating
def no_sweating(data, threshold=0.5, context_window=60, attr='EDA_0'):
    context = data[attr].iloc[-context_window:]
    max = context.max()
    # print(max)
    if max > threshold:
        return False
    else:
        return True


# determines whether the heart rate is in acceptable range
def heart_rate_ok(data, threshold=100, context_window=60, attr='HR_0'):
    context = data[attr].iloc[-context_window:]
    avg = np.average(context)
    if avg > threshold:
        return False
    else:
        return True


# determines whether there is any space in the car
def has_capacity(data):
    attributes = ['can1_AB_Gurtschloss_BF []', 'can1_AB_Gurtschloss_Reihe2_FA []', 'can1_AB_Gurtschloss_Reihe2_MI []', 'can1_AB_Gurtschloss_Reihe2_BF []']
    capacity = 0

    for name in attributes:
        context = data[name].iloc[-1]
        if context == 2:
            capacity += 1

    if capacity > 0:
        return True
    else:
        return False


# determines whether speed deviates by more than arbitrary threshold
def smooth_speed(data, threshold=10, context_window=60, attr='can0_ESP_v_Signal [Unit_KiloMeterPerHour]'):
    context = data[attr].iloc[-context_window:]
    stdv = np.std(context)
    if stdv > threshold:
        return False
    else:
        return True


# determines whether the driving behaviour is calm
def calm_driving(data, threshold=1000, context_window=60, attr='can0_MO_Drehzahl_01 [Unit_MinutInver]'):
    context = data[attr].iloc[-context_window:]
    avg = np.average(context)
    if avg > threshold:
        return False
    else:
        return True


if __name__ == "__main__":
    app.run()
