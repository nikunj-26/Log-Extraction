import os
import csv
import argparse
import re


# Taking inputs via command line(CLI)

parser = argparse.ArgumentParser(
    description='Input Format for Time : YYYY-MM-DD HH:MM:SS.  Enclose the parameters in " "')
parser.add_argument('-f', help='Starting Time', required=True)
parser.add_argument('-t', help='Ending Time', required=True)
parser.add_argument(
    '-i', help='Path to the directory of .log files', required=True)
args = vars(parser.parse_args())

# Function to convert the input string into searchable format : 2020-02-05 10:20:20  =>  2020-02-05T10:20:20


def inputformatter(s):
    # Replace all runs of whitespace with a single T
    s = re.sub(r"\s+", 'T', s)

    return s


start = inputformatter(args['f'])
end = inputformatter(args['t'])
path = args['i']
files = []
firstlines = []
loc_of_files = []


# LISTING ALL THE LOG FILES IN THE DIRECTORY
# r=root, d=directories, f = files


for r, d, f in os.walk(path):
    for file in f:
        if '.log' in file:
            files.append(os.path.join(r, file))

for f in files:
    with open(f) as fl:
        line = fl.readline().partition(".")
        firstlines.append(line[0])

# trying to print all the first lines ie the dates of the first line of all the files

# for f in firstlines:
#     print(f)

# Creating a dictionary where keys = Date in the first line of file, values = Path of the respective file

res = dict(zip(firstlines, files))
# print("Resultant Dictionary is : " + str(res))

# The function for extracting data


def extract_data(file_loc):
    reader = csv.reader(open(file_loc))
    filtered = filter(lambda p: p[0].split(
        '.')[0] >= start and p[0].split('.')[0] <= end, reader)
    for l in filtered:
        print(','.join(l))


# Finding the start file location

for dt in firstlines:
    if start < dt:
        start_file_index = firstlines.index(dt)-1
        start_file_date = firstlines[start_file_index]
        break
start_file_loc = res[start_file_date]
# print("Starting date :  "+start_file_date)
# print("Starting location :  "+start_file_loc)
# print("Start file index : "+str(start_file_index))

# Finding the end file location

for dt in firstlines:
    if dt > end:
        end_file_index = firstlines.index(dt)-1
        end_file_date = firstlines[end_file_index]
        break
end_file_loc = res[end_file_date]
# print("Ending date :  "+end_file_date)
# print("Ending file location :  "+end_file_loc)
# print("End file index : "+str(end_file_index))

# If start and end file are the same
if (start_file_index == end_file_index):
    extract_data(start_file_loc)
# Else if start and end files are one after another
elif((start_file_index+1) == end_file_index):
    extract_data(start_file_loc)
    extract_data(end_file_loc)
else:
    # Doing +1 as to include the last element in the list as well
    check_list = firstlines[start_file_index:(end_file_index+1)]
    for date in check_list:
        loc_of_files.append(res[date])
    for location in loc_of_files:
        extract_data(location)
