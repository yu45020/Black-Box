import os
import pandas as pd

"""
Splite a large CSV file into several small files and put them into a subfolder. Each small csv has header row
This script read the large csv file line by line to gurantee the data can be processed in memory limit .
User needs to specify the data location and names. 
    Example:
        split_csvs(filename='./task_data.csv', lines_per_block=200)

"""


def split_csvs(filename, out_folder=None, lines_per_block=10 ** 6):
    """
    :param filename: data file location with names. e.g. "./Data/cps_wages_LFP.csv"
    :param out_folder: splitted csvs location. e.g. "./Data/cps_wages_LFP_split/"
    :param lines_per_block: 10**6 # around 150 MB per csv file, but memory usage is around 15 MB.
    """
    # make subfolder
    path, file = os.path.split(filename)
    if not path:
        path = '.'
    if out_folder is None:
        out_folder = path + "/" + file.split(".")[0] + "_split/"
    file_counter = 1
    if not os.path.exists(out_folder):
        os.makedirs(out_folder)
    dat = pd.read_csv(filename, chunksize=lines_per_block, iterator=True)
    # dat.get_chunk()
    for dat_chunk in dat:
        print("Processing the {} split".format(file_counter))
        out_name = out_folder + file.split(".")[0] + "_{}".format(file_counter) + ".csv"
        dat_chunk.to_csv(out_name, index=True)
        file_counter += 1



