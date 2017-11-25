# -*- coding: utf-8 -*-
"""
Created on Thu Nov 16 17:28:44 2017
@author: Connor Dunne
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Nov 15 18:20:12 2017
@author: 10361551
"""

import pandas as pd
import numpy as np
from pandas import Series, DataFrame as df


def read_file(changes_file):
    # use strip to strip out spaces and trim the line.
    data = [line.strip() for line in open(changes_file, 'r')]
    return data
    
def get_commits(data):
    sep = 72*'-'
    #new_sep = "Changed paths:"
    commits = []
    #current_commit = None
    index = 0
    while index < len(data):
        try:
            #get counts of actions
            new_index = index + 3
            count_a = 0
            count_d = 0
            count_m = 0
            result = 1
            while result != 0:
                value = data[new_index][0]
                if value == "A":
                    count_a = count_a + 1
                elif value == "D":
                    count_d = count_d + 1
                elif value == "M":
                    count_m = count_m + 1
                new_index = new_index + 1   
                checker = data[new_index]
                result = len(checker)
                
            # parse each of the commits and put them into a list of commits
            details = data[index + 1].split('|')
            # the author with spaces at end removed.
            commit = {'revision': details[0].strip(),
                'author': details[1].strip(),
                'date': details[2].strip(),
                'number_of_lines': details[3].strip().split(' ')[0],
                "Add_Counts": count_a,
                "Delete_Counts": count_d,
                "Modify_Counts": count_m
            }
    
            # add details to the list of commits.
            commits.append(commit)
            
            #use index to locate sep position and start on next line   
            index = data.index(sep, index + 1)
        except IndexError:
            break
        
    dframe = pd.DataFrame(data = commits)
    return dframe

def clean_dates(dates):
    start_ind = "+"
    d_fixed = []
    for i in range(len(dates)):
        index = dates[i].index(start_ind)
        d_clean = dates[i][0:index-1]
        d_fixed.append(d_clean)
    return d_fixed

    
if __name__ == '__main__':
    # open the file - and read all of the lines.
    changes_file = 'changes_python.log'
    data = read_file(changes_file)
    commits = get_commits(data)
    d_fixed = clean_dates(commits["date"])
    commits["date"] = d_fixed
    commits['date'] = commits['date'].astype('datetime64[ns]')
    commits["Add_Counts"] = commits["Add_Counts"].astype(int)
    commits["Delete_Counts"] = commits["Delete_Counts"].astype(int)
    commits["Modify_Counts"] = commits["Modify_Counts"].astype(int)
    commits["number_of_lines"] = commits["number_of_lines"].astype(int)
    #commits["number_of_lines"].astype

    #commits["date"]
    # print the number of lines read
    ##print(len(data))
    #print(commits)
    ##print(commits[0])
    ##print(commits[1]['author'])
    ##print(len(commits))
    #type(commits_sorted["Add_Counts"][0])