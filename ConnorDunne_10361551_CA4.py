# -*- coding: utf-8 -*-
"""
Created on Wed Nov 15 18:20:12 2017
@author: Connor Dunne
@student_no: 10361551
@Description: Process, clean and analyse unstructured log data
"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

class LogFileImport(object):
    
    def read_file(self,changes_file):
        # use strip to strip out spaces and trim the line.
        data = [line.strip() for line in open(changes_file, 'r')]
        return data
        
    def get_commits(self,data):
        #create seperator by multiplying '-' by 72
        sep = 72*'-'
        commits = []
        #current_commit = None
        index = 0
        while index < len(data):
            try:
                #set index and count starts
                new_index = index + 3   #always 3 lines from main index
                count_a = 0
                count_d = 0
                count_m = 0
                result = 1
                while result != 0:   
                    #this will loop until result equals 0 meaning end of action log
                    #for each value found the count is increased and is reset for 
                    #the next loop
                    value = data[new_index][0]
                    if value == "A":
                        count_a = count_a + 1
                    elif value == "D":
                        count_d = count_d + 1
                    elif value == "M":
                        count_m = count_m + 1
                    new_index = new_index + 1   #move to next line
                    checker = data[new_index]
                    result = len(checker)   #if length is 0 no more lines to process
                    
                #parse each of the commits and put them into a list of commits
                details = data[index + 1].split('|')
                #the author with spaces at end removed
                commit = {'revision': details[0].strip(),
                    'author': details[1].strip(),
                    'date': details[2].strip(),
                    'number_of_lines': details[3].strip().split(' ')[0],
                    "Add_Counts": count_a,
                    "Delete_Counts": count_d,
                    "Modify_Counts": count_m
                }
        
                #add details to the list of commits.
                commits.append(commit)
                
                #use index to locate sep position and start on next line   
                index = data.index(sep, index + 1)
            except IndexError:
                break
        #convert to data frame and return data frame    
        dframe = pd.DataFrame(data = commits)
        return dframe
    
    def clean_dates(self,dates):
        #remove everything after the '+' symbol in dates
        #only interested in date and time at beginning
        start_ind = "+"
        d_fixed = []
        for i in range(len(dates)):
            index = dates[i].index(start_ind)
            d_clean = dates[i][0:index-1]
            d_fixed.append(d_clean)
        return d_fixed

    
if __name__ == "__main__":
    ##open the file - and read all of the lines using LogFileImport module
    Importer = LogFileImport()
    changes_file = "changes_python.log"
    data = Importer.read_file(changes_file)
    commits = Importer.get_commits(data)
    d_fixed = Importer.clean_dates(commits["date"])
    #dates cleaned and convert columns to appropriate data types
    commits["date"] = d_fixed
    commits["date"] = commits["date"].astype("datetime64[ns]")
    commits["Add_Counts"] = commits["Add_Counts"].astype(int)
    commits["Delete_Counts"] = commits["Delete_Counts"].astype(int)
    commits["Modify_Counts"] = commits["Modify_Counts"].astype(int)
    commits["number_of_lines"] = commits["number_of_lines"].astype(int)
    
    #1
    ##descriptive statistics
    com_describe = commits.describe()   #descriptive stats
    com_sum = commits.sum()   #return sum of values
    unique_auth = set(commits["author"])   #set function returns set of unique values
    unique_rev = set(commits["revision"])
    len(unique_auth)   #get the lengths for the number of unique values
    len(unique_rev)
    
    #2
    ##actions per user
    name_list = []
    for i in unique_auth:
        #for each unique author locate author name and return sum of each action
        acounts_name = commits.loc[commits["author"]==i,"Add_Counts"].sum()
        mcounts_name = commits.loc[commits["author"]==i,"Modify_Counts"].sum()
        dcounts_name = commits.loc[commits["author"]==i,"Delete_Counts"].sum()
        #append to list of dictionaries for each author and action counts
        name_list.append({"author":i,"add":acounts_name,"modify":mcounts_name,"delete":dcounts_name})
    
    #convert to dataframe
    name_counts = pd.DataFrame(data = name_list)
    #set author name as index on the dataframe
    name_counts = name_counts.set_index("author")
    #print bar plot of each action count by authors
    bar_plot = name_counts[["add","modify","delete"]].plot(kind = "bar",title = "Author Counts",legend = True,figsize=(10, 5))
    
    #3
    ##time series analysis
    #sort values by date
    commits_sorted = commits.sort_values(by = "date")
    #create lists of action counts
    add_counts_list = commits_sorted["Add_Counts"].tolist()
    delete_counts_list = commits_sorted["Delete_Counts"].tolist()
    modify_counts_list = commits_sorted["Modify_Counts"].tolist()
    #create date series for each list of actions
    TS_Add = pd.Series(add_counts_list,index =commits_sorted["date"])
    TS_Modify = pd.Series(modify_counts_list,index =commits_sorted["date"])
    TS_Delete = pd.Series(delete_counts_list,index =commits_sorted["date"])
    #resample the data by week
    TS_AddW = TS_Add.resample('W').sum()
    TS_ModifyW = TS_Modify.resample('W').sum()
    TS_DeleteW = TS_Delete.resample('W').sum()
    #create data frame containing all series
    action_times = pd.DataFrame({"Add":TS_Add,"Modify":TS_Modify,"Delete":TS_Delete})
    #plot time series graph on one plot
    action_times.plot(title = "Time Series")
    #plot time series graph with 3 seperate sub plots
    action_times.plot(title = "Time Series", subplots=True)
    action_corr = action_times.corr()
    sns.heatmap(action_corr,cmap=sns.diverging_palette(220, 10, as_cmap=True),square=True)