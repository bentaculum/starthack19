import pandas as pd
import os
import glob
import numpy as np
import time
import csv

def load_csvs(dir_car, dir_watch):
    """ load all data from csv files, adapt sampling frequencies to 1 second and merge together

    we assume that the directories contain only the desired files.
    we round all time values to full second granularity and then drop duplicates on the time dimension
    we work with relative timestamps, starting at 0 seconds

    Parameters
    ----------
    dir_car : string
        absolute path to the directory with all the car csvs
    dir_watch : string
        absolute path to the directory with all the watch csvs

    Returns
    -------
    pandas DataFrame

    """

    os.chdir(dir_car)
    files = [i for i in glob.glob('*_DataGroup_*.csv')]

    df_car = pd.DataFrame()
    for f in files:
        print('loading {} ...'.format(f))
        df = pd.read_csv(f)
        df.time = np.floor(df.time)
        #         print(len(df.time))
        df = df.drop_duplicates(subset=['time'])
        df = df.set_index('time', drop=True, append=False)
        #         print(df.shape)
        try:
            df_car = pd.concat([df_car, df], axis=1, join='outer')
        except KeyError:
            df_car = df
    #         print(df_car.shape)

    os.chdir(dir_watch)
    files = [i for i in glob.glob('*.csv')]

    samp_freq_dict = {
        'BVP': 64,
        'HR': 1,
        'EDA': 4,
        'TEMP': 4,
        'ACC': 32,
    }

    #     df.iloc[::5, :]

    df_watch = pd.DataFrame()
    for f in files:
        print('loading {} ...'.format(f))
        filename = f.split('.')[-2]
        df = pd.read_csv(f)
        df = df.iloc[::samp_freq_dict[filename], :]
        #         print(df.shape)
        df = df.reset_index(drop=True)
        df.index.name = 'time'
        df.columns = ['{}_{}'.format(filename, x) for x in range(df.shape[1])]
        #         display(df)

        try:
            df_watch = pd.concat([df_watch, df], axis=1, join='outer')
        except KeyError:
            df_watch = df
    #         print(df_watch.shape)
    #     display(df_watch.head())

    df_watch.index.name = 'time'
    #     display(df_watch)
    # merge car and watch data
    df_all = pd.concat([df_watch, df_car], axis=1, join='inner')

    return df_all


# write one additional row of the data table to csv
def stream_to_csv(df, csv_path, csv_name, update_interval=1):
    """ simulate stream that writes to csv file once per second

    we assume that the directories contain only the desired files.
    we round all time values to full second granularity and then drop duplicates on the time dimension
    we work with relative timestamps, starting at 0 seconds

    Parameters
    ----------
    df : DataFrame
        table with all data
    csv_path : string
        directory of out csv
    csv_name : string
        name of out csv
    update_interval : float
        waiting time in seconds until the next row is appended to the csv

    """
    # make sure the time is also written
    df = df.reset_index()
    n_rows = df.shape[0]
    counter = 0

    # remove old file, or create directory
    if os.path.isdir(csv_path):
        if os.path.isfile(os.path.join(csv_path, csv_name)):
            os.remove(os.path.join(csv_path, csv_name))
    else:
        os.makedirs(csv_path)

    # write header
    with open(os.path.join(csv_path, csv_name), 'w') as f:
        writer = csv.writer(f)
        #         print(df.columns.tolist())
        writer.writerow(df.columns.tolist())

    while counter < n_rows:
        with open(os.path.join(csv_path, csv_name), 'a') as f:
            writer = csv.writer(f)
            #             print(df.iloc[counter,:].values.tolist())
            writer.writerow(df.iloc[counter, :].values.tolist())
        # print('received row {}'.format(counter))
        time.sleep(update_interval)
        counter += 1
    print('stream ended')
