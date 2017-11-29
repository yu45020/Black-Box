import csv
import os

# Splite a large CSV file into several small files and put them into a subfolder. Each small csv has header row
# This script read the large csv file line by line to gurantee the data can be processed in memory limit .
# User needs to specify the data location and names. 

def get_chunk_csv(lines,csvreader,counter):
    """
	Read the large csv file line by line and write them into a csv file. 
	
    :param lines: max lines per chunk
    :param csvreader: a csv reader
    :param counter: a splited csv file number
    :return: a chunk of csv data
    """
    outfile = out_folder+str(counter)+'.csv'
    with open(outfile, "w", newline="") as f: 
        # newline setting makes no blank lines in the output
        csvwriter = csv.writer(f)
        csvwriter.writerow(header)
        for i in range(lines):
            try:
                line = next(csvreader)
            except StopIteration:
                global last_line
                last_line = True
                print('Done')
                break
            csvwriter.writerow(line)

def split_csvs(filename, out_folder, lines_per_block=10**6 ):
    """
    :param filename: data file location with names. e.g. "./Data/cps_wages_LFP.csv"
    :param out_folder: splitted csvs location. e.g. "./Data/cps_wages_LFP_split/"
    :param lines_per_block: 10**6 # around 150 MB per csv file, but memory usage is around 15 MB.  
    """
    # make subfolder
    if not os.path.exists(out_folder): 
        os.makedirs(out_folder)

    with open(filename,newline="") as file_to_split:
        data = csv.reader(file_to_split)
        header = next(data)
        last_line = False
        counter = 1
        while not last_line:
            print('Splitting file '+str(counter))
            chunk_data = get_chunk_csv(lines_per_block,data,counter)
            counter +=1
        