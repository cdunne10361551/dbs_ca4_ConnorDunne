# -*- coding: utf-8 -*-
"""
Created on Sat Nov 25 12:01:59 2017

@author: connor
"""

#time series analysis
commits_sorted = commits.sort_values(by = "date")
#commits.plot(commits_sorted["Add_Counts"],commits_sorted["date"])
add_counts_list = pd.to_numeric(commits_sorted["Add_Counts"].tolist())
delete_counts_list = pd.to_numeric(commits_sorted["Delete_Counts"].tolist())
modify_counts_list = pd.to_numeric(commits_sorted["Modify_Counts"].tolist())
TS_Add = Series(add_counts_list,index =commits_sorted["date"])
TS_Modify = Series(modify_counts_list,index =commits_sorted["date"])
TS_Delete = Series(delete_counts_list,index =commits_sorted["date"])
TS_AddW = TS_Add.resample('W').sum()
TS_ModifyW = TS_Modify.resample('W').sum()
TS_DeleteW = TS_Delete.resample('W').sum()
action_times = df({"Add":TS_Add,"Modify":TS_Modify,"Delete":TS_Delete})
action_times.plot(title = "Time Series")
action_times.plot(title = "Time Series", subplots=True)
#commits.type
    
#descriptive statistics
com_describe = commits.describe()
com_sum = commits.sum()
unique_auth = set(commits["author"])
unique_rev = set(commits["revision"])
len(unique_auth)
len(unique_rev)
#commits.var()
#commits.std()
#commits.skew()
#commits.kurt()
#commits.corr()
#skew = commits.skew()
#print skew
#commits.boxplot()

#actions per user
#import matplotlib as mt
#from matplotlib import pyplot as plt
name_list = []
for i in unique_auth:
    acounts_name = commits.loc[commits["author"]==i,"Add_Counts"].sum()
    mcounts_name = commits.loc[commits["author"]==i,"Modify_Counts"].sum()
    dcounts_name = commits.loc[commits["author"]==i,"Delete_Counts"].sum()
    name_list.append({"author":i,"add":acounts_name,"modify":mcounts_name,"delete":dcounts_name})

name_counts = pd.DataFrame(data = name_list)
name_counts = name_counts.set_index("author")
bar_plot = name_counts[["add","modify","delete"]].plot(kind = "bar",title = "Author Counts",legend = True,figsize=(10, 5))
pie_plot = name_counts[["add"]].plot(kind = "pie",title = "Author Counts",subplots=True, legend = False)
pie_plot = name_counts[["modify"]].plot(kind = "pie",title = "Author Counts",subplots=True,legend = False)
pie_plot = name_counts[["delete"]].plot(kind = "pie",title = "Author Counts",subplots=True,legend = False)
figure = plot_count.get_figure()
figure.savefig("output.png")