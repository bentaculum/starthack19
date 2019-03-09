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


# run_with_ngrok(app)

url = "http://130.82.239.210"

#@app.route("/driver")
# def driver_ready():
#     if has_capacity() & calm_driving() & smooth_speed() & heart_rate_ok() & no_sweating():
#         return True
#     else:
#         return False
#
#
# # HELPER FUNCTIONS BELOW
#
# # determines whether the driver is not excessively sweating
# def no_sweating(threshold):
#     # TODO: max sweat level from last 60 seconds
#     if max > threshold:
#         return False
#     else:
#         return True
#
#
# # determines whether the heart rate is in acceptable range
# def heart_rate_ok(threshold):
#     # TODO: average from last 60 seconds
#     if avg > threshold:
#         return False
#     else:
#         return True
#
#
# # determines whether there is any space in the car
# def has_capacity():
#     # TODO: get data from CSV (last cell available)
#     attributes = ['AB_Gurtschloss_BF', 'AB_Gurtschloss__Reihe2_FA', 'AB_Gurtschloss__Reihe2_MI', 'AB_Gurtschloss__Reihe2_BF']
#     capacity = 0
#
#     for name in attributes:
#         r = requests.get(url + '/signal/' + name + '/value')
#         data = json.loads(json.dumps(r.json()))
#         try:
#             if data.get('measurement').get('value') == 2:
#                 capacity += 1
#         except:
#             continue
#     if capacity > 0:
#         return True
#     else:
#         return False
#
#
# # determines whether speed deviates by more than arbitrary threshold
# # TODO: use speed limits on given roads
# def smooth_speed(threshold=30):
#     # TODO: get data from CSV, if stdv above threshold, False
#     if stdv > threshold:
#         return False
#     else:
#         return True
#
#
# # determines whether the driving behaviour is calm
# # threshold is an arbitrary value for now, could be ml
# def calm_driving(threshold=1000):
#     # TODO: use average values from last 60 seconds
#     r = requests.get(url + '/signal/MO_Drehzahl_01/value')
#     data = json.loads(json.dumps(r.json()))
#     avg = data.get('measurement').get('value')
#
#     if avg > threshold:
#         return False
#     else:
#         return True



if __name__ == "__main__":
    app.run()
