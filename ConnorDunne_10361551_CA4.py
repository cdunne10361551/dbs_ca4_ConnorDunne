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
from pandas import Series, DataFrame, Panel
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
        
    df = pd.DataFrame(data = commits)
    return df

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

    commits["date"]
    # print the number of lines read
    ##print(len(data))
    #print(commits)
    ##print(commits[0])
    ##print(commits[1]['author'])
    ##print(len(commits))
    #type(commits_sorted["Add_Counts"][0])
    
    #time series analysis
    commits['date'] = commits['date'].astype('datetime64[ns]')
    commits["Add_Counts"] = pd.to_numeric(commits["Add_Counts"])
    commits_sorted["number_of_lines"] = pd.to_numeric(commits_sorted["number_of_lines"])
    pd.to_numeric(commits["Delete_Counts"])
    pd.to_numeric(commits["Modify_Counts"])
    commits_sorted = commits.sort_values(by = "date")
    dates = pd.date_range('2015-07', '2015-12', freq='D')
    AO = Series(commits_sorted["Add_Counts"], index=commits_sorted["date"])
    commits.plot(commits_sorted["Add_Counts"],commits_sorted["date"])
    add_counts_list = pd.to_numeric(commits_sorted["Add_Counts"].tolist())
    delete_counts_list = pd.to_numeric(commits_sorted["Delete_Counts"].tolist())
    modify_counts_list = pd.to_numeric(commits_sorted["Modify_Counts"].tolist())
    AO_Add = Series(add_counts_list,index =commits_sorted["date"])
    AO_Modify = Series(modify_counts_list,index =commits_sorted["date"])
    AO_Delete = Series(delete_counts_list,index =commits_sorted["date"])
    AO_Add.plot()
    AO_Modify.plot()
    AO_Delete.plot()
    AO_AddW = AO_Add.resample('W').sum()
    AO_ModifyW = AO_Modify.resample('W').sum()
    AO_DeleteW = AO_Delete.resample('W').sum()
    action_times = DataFrame({"AO_Add":AO_Add,"AO_Modify":AO_Modify,"AO_Delete":AO_Delete})
    action_times.plot()
    action_times.plot(subplots=True)
    action_timesW = DataFrame({"AO_Add":AO_AddW,"AO_Modify":AO_ModifyW,"AO_Delete":AO_DeleteW})
    action_timesW.plot()
    action_timesW.plot(subplots=True)
    commits.type
    
    #descriptive statistics
    commits_sorted.sum()
    commits_sorted.mean()
    commits_sorted["Add_Counts"].cumsum()
    commits_sorted["Modify_Counts"].cumsum()
    commits_sorted["Delete_Counts"].cumsum()
    commits_sorted.describe()
    commits_sorted.var()
    commits_sorted.std()
    commits_sorted.skew()
    commits_sorted.kurt()
    commits_sorted.corr()
    skew = commits_sorted.skew()
    print skew
    commits_sorted.boxplot()
    
    mean = np.mean(elements, axis=0)
    sd = np.std(elements, axis=0)
    add_list = commits_sorted["Add_Counts"]
    elements = np.array(commits_sorted["Add_Counts"])
    final_list = [x for x in add_list if (x > mean - 2 * sd)]
    final_list = [x for x in final_list if (x < mean + 2 * sd)]
    skew = final_list.skew()
    print skew
    final_list.boxplot()
    
    
    #actions per user
    commits_sorted["Add_Counts"].sum()
    commits_sorted.loc[commits_sorted["author"]=="Thomas","Delete_Counts"].sum()