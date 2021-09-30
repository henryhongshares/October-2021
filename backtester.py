import pandas as pd
import math
import os.path
import time
from binance.client import Client
from datetime import timedelta, datetime
from dateutil import parser
from tqdm import tqdm_notebook #(Optional, used for progress-bars)



binance_api_key = 'VFUpZTZCaXPz8ScCWm0yhkRW3J8VqGr9pPAlpXEVIclkeRDPjp7z8xtQmS2sfQWS'    #Enter your own API-key here
binance_api_secret = 'kuNwSWkQ03T2wl7jbqpqrdMO6B7LVH8joBxJopzlWbPVaxJDKWRZsQrnFocimPvW' #Enter your own API-secret here

### CONSTANTS
binsizes = {"1m": 1, "5m": 5, "1h": 60, "1d": 1440}
batch_size = 750
binance_client = Client(api_key=binance_api_key, api_secret=binance_api_secret)


### FUNCTIONS
def minutes_of_new_data(symbol, kline_size, data, source):
    if len(data) > 0:  old = parser.parse(data["timestamp"].iloc[-1])
    elif source == "binance": old = datetime.strptime('1 Jan 2017', '%d %b %Y')
    elif source == "binanceFutures": old = datetime.strptime('8 Sep 2019', '%d %b %Y')
    elif source == "bitmex": old = bitmex_client.Trade.Trade_getBucketed(symbol=symbol, binSize=kline_size, count=1, reverse=False).result()[0][0]['timestamp']
    if source == "binance": new = pd.to_datetime(binance_client.get_klines(symbol=symbol, interval=kline_size)[-1][0], unit='ms')
    if source == "binanceFutures": new = pd.to_datetime(binance_client.get_klines(symbol=symbol, interval=kline_size)[-1][0], unit='ms')
    if source == "bitmex": new = bitmex_client.Trade.Trade_getBucketed(symbol=symbol, binSize=kline_size, count=1, reverse=True).result()[0][0]['timestamp']
    return old, new

def get_all_binanceFutures(symbol, kline_size, save = False):
    filename = '%s-%s-%s-data.csv' % (symbol, 'futures', kline_size)
    if os.path.isfile(filename): data_df = pd.read_csv(filename)
    else: data_df = pd.DataFrame()
    oldest_point, newest_point = minutes_of_new_data(symbol, kline_size, data_df, source = "binanceFutures")
    delta_min = (newest_point - oldest_point).total_seconds()/60
    available_data = math.ceil(delta_min/binsizes[kline_size])
    if oldest_point == datetime.strptime('8 Sep 2019', '%d %b %Y'): print('Downloading all available %s data for %s. Be patient..!' % (kline_size, symbol))
    else: print('Downloading %d minutes of new data available for %s, i.e. %d instances of %s data.' % (delta_min, symbol, available_data, kline_size))
    klines = binance_client.get_historical_futures_klines(symbol, kline_size, oldest_point.strftime("%d %b %Y %H:%M:%S"), newest_point.strftime("%d %b %Y %H:%M:%S"))
    data = pd.DataFrame(klines, columns = ['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_av', 'trades', 'tb_base_av', 'tb_quote_av', 'ignore' ])
    data['timestamp'] = pd.to_datetime(data['timestamp'], unit='ms')
    if len(data_df) > 0:
        temp_df = pd.DataFrame(data)
        data_df = data_df.append(temp_df)
    else: data_df = data
    data_df.set_index('timestamp', inplace=True)
    if save: data_df.to_csv(filename)
    print('All caught up..!')
    return data_df

def get_all_binance(symbol, kline_size, save = False):
    filename = '%s-%s-data.csv' % (symbol, kline_size)
    if os.path.isfile(filename): data_df = pd.read_csv(filename)
    else: data_df = pd.DataFrame()
    oldest_point, newest_point = minutes_of_new_data(symbol, kline_size, data_df, source = "binance")
    delta_min = (newest_point - oldest_point).total_seconds()/60
    available_data = math.ceil(delta_min/binsizes[kline_size])
    if oldest_point == datetime.strptime('1 Jan 2017', '%d %b %Y'): print('Downloading all available %s data for %s. Be patient..!' % (kline_size, symbol))
    else: print('Downloading %d minutes of new data available for %s, i.e. %d instances of %s data.' % (delta_min, symbol, available_data, kline_size))
    klines = binance_client.get_historical_klines(symbol, kline_size, oldest_point.strftime("%d %b %Y %H:%M:%S"), newest_point.strftime("%d %b %Y %H:%M:%S"))
    data = pd.DataFrame(klines, columns = ['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_av', 'trades', 'tb_base_av', 'tb_quote_av', 'ignore' ])
    data['timestamp'] = pd.to_datetime(data['timestamp'], unit='ms')
    if len(data_df) > 0:
        temp_df = pd.DataFrame(data)
        data_df = data_df.append(temp_df)
    else: data_df = data
    data_df.set_index('timestamp', inplace=True)
    if save: data_df.to_csv(filename)
    print('All caught up..!')
    return data_df




ticker = timeframe = (input("Which ticker? Enter here: "))
timeframe = (input("Which time frame, 1m, 5m, 1h, 1d? Enter here: "))

get_all_binance(ticker, timeframe, save = True)

##############################################################################################################################



print('Importing Libraries')
from itertools import zip_longest
import matplotlib.pyplot as plt
import scipy.stats as stats
import numpy as np
import csv
import pandas as pd
import numpy as np


print('1) Opening Excel file')
preffix= '-'
suffix = '-data.csv'
combine = ticker + preffix + timeframe + suffix

data = open (combine ,encoding = 'utf-8')
csv_data = csv.reader(data)

Doc= list (csv_data)


# 1) opens the file 
# 2) translates the csv
# 3) translates csv into list of lists

print('2) Headers are:')

for x in Doc[0]:
    z = "-  "
    print(z + x) 


print('3) Processing time from string to integer')
# create time from len Doc:
time_cleaned =list(range(1,len(Doc)))    

date=[]
minutes=[]
date_and_minute_paired_list= []
print('4) Processing date from string to integer')
for row in Doc[1:]:
    date_and_minute_paired_list.append(row[0].split(' '))

for row in date_and_minute_paired_list:
    date.append(row[0])
    minutes.append(row[1])

print('5) Processing prices from string to integer')

# Large data set prices are given to us as strings but we want float so we must clean data:
large_data_set_cleaned =[]    

for row in Doc[1:]:
        large_data_set_cleaned.append(float(row[1]))

print('6) Defining sample data')

today =len(Doc)
print(f"right now is is {today}")

yesterday = len(Doc)-1440
print(f"yesterday is {yesterday}")


print('sample_start = 595156')
print('sample_finish = 596016')


# Define the Sample data:

sample_start = int(input("Enter sample start number: "))
sample_finish = int(input("Enter sample finish number: "))
sample_length= (sample_finish-sample_start)

#  TODAY'S FORECAST:
# 
#present_time = time_cleaned[-1] 
#a_day_before_present_time = present_time - (1*60*24)
#sample_start = a_day_before_present_time
#sample_finish = present_time
#sample_length= (sample_finish-sample_start)
# Sample prices are given to us as strings but we want float so we must clean data:
sample_cleaned = []

for row in Doc[sample_start:sample_finish]:
    sample_cleaned.append(float(row[4]))
    
sample_length

print("7) Please wait while the CORRELATION CALCULATION ITERATION is running should take 6.5 mins ")


# PERFORMING CORRELATION CALCULATION ITERATION with our sample_cleaned

large_data_set_cleaned
window_size = sample_length

i = 0
moving_correlation=[]
while i <len(large_data_set_cleaned) -window_size +1:
    this_window = large_data_set_cleaned[i : i + window_size]
    
    window_correlation= correlation, p_value = stats.pearsonr(this_window, sample_cleaned)
    moving_correlation.append(window_correlation)
    i += 1
    
# output (moving_correlation) appears to be a list of tuples?? with 2 elements inside the tuple? I was expecting one list of single floats??
# after checking the numbers I found that we only need the 1st number as it matches with the csv figures!

print('8) All finished, check your browser for the results!')


correlations = []

for item in moving_correlation:
    correlations.append(item[0])
# we have extracted the first number in the tuples to lists

pd.set_option("display.max_rows", 20)

initial_df = pd.DataFrame(time_cleaned,columns = ["Time Index"])
initial_df = initial_df.set_index('Time Index')
initial_df["Date"]= date
initial_df["Minute "]= minutes
initial_df["Close Price "]= large_data_set_cleaned

barry =[0] * (sample_length-1)
barry.extend(correlations)
initial_df["Correlation"]= barry

initial_df

initial_df.Correlation = initial_df.Correlation.astype(float)
initial_sorted_df = initial_df.sort_values(['Correlation'], ascending=[False])
initial_sorted_df

# create the dictionary for {time_cleaned : [date,minute]}

date_and_minute_dictionary=dict(zip_longest(time_cleaned, date_and_minute_paired_list))
date_and_minute_dictionary

# TIME + DATE DICTIONARY
time_and_date_dictionary=dict(zip_longest(time_cleaned, date))
time_and_date_dictionary

# TIME + MINUTES DICTIONARY
time_and_minutes_dictionary=dict(zip_longest(time_cleaned, minutes))
time_and_minutes_dictionary

# TIME + CLOSE PRICE DICTIONARY
time_and_close_price_dictionary=dict(zip_longest(time_cleaned, large_data_set_cleaned))
time_and_close_price_dictionary

# TIME + CORRELATION DICTIONARY
time_and_correlation_dictionary=dict(zip_longest(time_cleaned,barry))


time_by_descending_correlation = initial_sorted_df.index.tolist()
descending_correlation = initial_sorted_df.Correlation.tolist()

# IMPRESSIVE!, this code removes all the overlapping, takes value of list look left by increment, looks right by increment
# purges all those left and right, looks at the next and does the same, remember that this works because our list has already
# been sorted from when we created the time_and_correlation_dictionary_sorted
# was the only way we could delete/purge/remove overlaps since we could not operate on a dictionary, cannot loop on a dictionary
# 1 filteredtime
increment = sample_length

to_remove = set()
for x in time_by_descending_correlation:
    if x not in to_remove:
        # Number is not going to be removed by previous, so it's going to be
        # the next purge candidate.
        for i in range(1, 1 + increment):
            to_remove.add(x - i)
            to_remove.add(x + i)

filtered_time = [x for x in time_by_descending_correlation if x not in to_remove]

# to construct it back into easy to read dictionary format we now find corresponding, correlation, date and finally minutes
# 1 filteredcorrelation:

filtered_date = [time_and_date_dictionary[x] for x in filtered_time]
filtered_minute = [time_and_minutes_dictionary[x] for x in filtered_time]
filtered_correlations = [time_and_correlation_dictionary[x] for x in filtered_time]
filtered_close_price = [time_and_close_price_dictionary[x] for x in filtered_time]


pd.set_option("display.max_rows", 600)

filtered_df = pd.DataFrame(filtered_time,columns = ["Time Index"])
filtered_df = filtered_df.set_index('Time Index')
filtered_df["Dates"]= filtered_date
filtered_df["Minutes"]= filtered_minute
filtered_df["Correlations"]= filtered_correlations
filtered_df["Close Price"] = filtered_close_price
filtered_df

#INPUTS! INPUTS! INPUTS! INPUTS! INPUTS! INPUTS! INPUTS! INPUTS! INPUTS! INPUTS! INPUTS! INPUTS! INPUTS! INPUTS! 
######################################################################################################################
berry = 8
leap = 0 *berry


dataset1end   =      filtered_time[1+leap]                    
dataset1start =  dataset1end - sample_length   
                                               
dataset2end   =      filtered_time[2+leap]                     
dataset2start =  dataset2end - sample_length   
                                               
dataset3end   =      filtered_time[3+leap]               
dataset3start =  dataset3end - sample_length

dataset4end   =      filtered_time[4+leap]               
dataset4start=  dataset4end - sample_length

dataset5end   =       filtered_time[5+leap]               
dataset5start =  dataset5end - sample_length

dataset6end   =      filtered_time[6+leap]              
dataset6start =  dataset6end - sample_length

dataset7end   =       filtered_time[7+leap]            
dataset7start =  dataset7end - sample_length

dataset8end   =       filtered_time[8+leap]              
dataset8start =  dataset8end - sample_length


future_projection = 700                          #######################################################################
                                               #######################################################################  
######################################################################################################################
X = []
Y = []
A = []
B = []
C = []
D = []
E = []
F = []
G = []
H = []
I = []
J = []
K = []
L = []
M = []
N = []
O = []
P = []

# List Loops for Plotting     
#########################################################################################################################

# For our Sample Data (sample):    
for element in time_cleaned[sample_start:sample_finish]:
    X.append(element)    
for element in sample_cleaned:
    Y.append(element)
    
# For our Data Set 1 (large_data_set)
for element in time_cleaned[dataset1start:dataset1end + future_projection]:
    A.append(element)
for element in large_data_set_cleaned[dataset1start:dataset1end + future_projection]:
    B.append(element)
    
# For our Data Set 2 (large_data_set):       
for element in time_cleaned[dataset2start:dataset2end + future_projection]:
    C.append(element)
for element in large_data_set_cleaned[dataset2start:dataset2end + future_projection]:
    D.append(element)
    
# For our Data Set 3 (large_data_set):       
for element in time_cleaned[dataset3start:dataset3end + future_projection]:
    E.append(element)
for element in large_data_set_cleaned[dataset3start:dataset3end + future_projection]:
    F.append(element)
    
    #######################################
    
for element in time_cleaned[dataset4start:dataset4end + future_projection]:
    G.append(element)
for element in large_data_set_cleaned[dataset4start:dataset4end + future_projection]:
    H.append(element)

for element in time_cleaned[dataset5start:dataset5end + future_projection]:
    I.append(element)
for element in large_data_set_cleaned[dataset5start:dataset5end + future_projection]:
    J.append(element)
    
for element in time_cleaned[dataset6start:dataset6end + future_projection]:
    K.append(element)
for element in large_data_set_cleaned[dataset6start:dataset6end + future_projection]:
    L.append(element)
    
for element in time_cleaned[dataset7start:dataset7end + future_projection]:
    M.append(element)
for element in large_data_set_cleaned[dataset7start:dataset7end + future_projection]:
    N.append(element)
    
for element in time_cleaned[dataset8start:dataset8end + future_projection]:
    O.append(element)
for element in large_data_set_cleaned[dataset8start:dataset8end + future_projection]:
    P.append(element)


from bokeh.layouts import gridplot
from bokeh.io import output_file, show
from bokeh.plotting import figure
from bokeh.models import FreehandDrawTool

output_file("Top_8_Matches.html")

TOOLS = "crosshair,pan,wheel_zoom,box_zoom,reset,box_select,lasso_select,poly_select,save,undo"

# create a new plot

Sample_Data = figure(tools=TOOLS, width=600, x_axis_label='TIME', y_axis_label='PRICE',  plot_height=400, title= f"SAMPLE DATA {sample_finish} -     {date_and_minute_dictionary[sample_finish]}          Correlation  {time_and_correlation_dictionary[sample_finish]}  ")
Sample_Data.line(X, Y, line_width=3, color="black", alpha=1)
Sample_Data.ygrid.grid_line_color = None
Sample_Data.ygrid.grid_line_color = None

ticks = [sample_finish]
Sample_Data.xaxis[0].ticker = ticks
Sample_Data.xgrid[0].ticker = ticks
Sample_Data.xgrid.band_fill_alpha  = 0.1
Sample_Data.xgrid.band_fill_color = "navy"


renderer = Sample_Data.multi_line([[sample_start, sample_start+1]], [[Y[0], Y[1]]], line_width=5, alpha=0.4, color='red')
draw_tool = FreehandDrawTool(renderers=[renderer], num_objects=10)
Sample_Data.add_tools(draw_tool)
Sample_Data.toolbar.active_drag = draw_tool


Data_Set_1 = figure(tools=TOOLS, width=600, x_axis_label='TIME', y_axis_label='PRICE',   height=400, title= f"Data Set 1 - {dataset1end} -    {date_and_minute_dictionary[dataset1end]}         Correlation  {time_and_correlation_dictionary[dataset1end]}  ")
Data_Set_1.line(A, B, line_width=1, color="navy", alpha=1)
Data_Set_1.ygrid.grid_line_color = None
Data_Set_1.ygrid.grid_line_color = None
ticks = [0,1, dataset1end]
Data_Set_1.xaxis[0].ticker = ticks
Data_Set_1.xgrid[0].ticker = ticks
Data_Set_1.xgrid.band_fill_alpha  = 0.1
Data_Set_1.xgrid.band_fill_color = "navy"

renderer = Data_Set_1.multi_line([[dataset1start, dataset1start+1]], [[B[0], B[1]]], line_width=5, alpha=0.4, color='red')
draw_tool = FreehandDrawTool(renderers=[renderer], num_objects=10)
Data_Set_1.add_tools(draw_tool)
Data_Set_1.toolbar.active_drag = draw_tool

Data_Set_2 = figure(tools=TOOLS, width=600, x_axis_label='TIME', y_axis_label='PRICE',  height=400, title= f"Data Set 2 - {dataset2end} -     {date_and_minute_dictionary[dataset2end]}          Correlation  {time_and_correlation_dictionary[dataset2end]}  ")
Data_Set_2.line(C, D, line_width=1, color="deeppink", alpha=1)
ticks = [0,1, dataset2end]
Data_Set_2.xaxis[0].ticker = ticks
Data_Set_2.xgrid[0].ticker = ticks
Data_Set_2.xgrid.band_fill_alpha  = 0.1
Data_Set_2.xgrid.band_fill_color = "navy"

renderer = Data_Set_2.multi_line([[dataset2start, dataset2start+1]], [[D[0], D[1]]], line_width=5, alpha=0.4, color='red')
draw_tool = FreehandDrawTool(renderers=[renderer], num_objects=10)
Data_Set_2.add_tools(draw_tool)
Data_Set_2.toolbar.active_drag = draw_tool

Data_Set_3 = figure(tools=TOOLS, width=600, x_axis_label='TIME', y_axis_label='PRICE',  height=400, title= f"Data Set 3 - {dataset3end} -     {date_and_minute_dictionary[dataset3end]}          Correlation  {time_and_correlation_dictionary[dataset3end]}  ")
Data_Set_3.line(E, F, line_width=1, color="green", alpha=1)
ticks = [0,1, dataset3end]
Data_Set_3.xaxis[0].ticker = ticks
Data_Set_3.xgrid[0].ticker = ticks
Data_Set_3.xgrid.band_fill_alpha  = 0.1
Data_Set_3.xgrid.band_fill_color = "navy"

renderer = Data_Set_3.multi_line([[dataset3start, dataset3start+1]], [[F[0], F[1]]], line_width=5, alpha=0.4, color='red')
draw_tool = FreehandDrawTool(renderers=[renderer], num_objects=10)
Data_Set_3.add_tools(draw_tool)
Data_Set_3.toolbar.active_drag = draw_tool


Data_Set_4 = figure(tools=TOOLS, width=600, x_axis_label='TIME', y_axis_label='PRICE',  height=400, title= f"Data Set 4 - {dataset4end} -     {date_and_minute_dictionary[dataset4end]}          Correlation  {time_and_correlation_dictionary[dataset4end]}  ")
Data_Set_4.line(G, H, line_width=1, color="firebrick", alpha=1)
ticks = [0,1, dataset4end]
Data_Set_4.xaxis[0].ticker = ticks
Data_Set_4.xgrid[0].ticker = ticks
Data_Set_4.xgrid.band_fill_alpha  = 0.1
Data_Set_4.xgrid.band_fill_color = "navy"

renderer = Data_Set_4.multi_line([[dataset4start, dataset4start+1]], [[H[0], H[1]]], line_width=5, alpha=0.4, color='red')
draw_tool = FreehandDrawTool(renderers=[renderer], num_objects=10)
Data_Set_4.add_tools(draw_tool)
Data_Set_4.toolbar.active_drag = draw_tool


Data_Set_5 = figure(tools=TOOLS, width=600, x_axis_label='TIME', y_axis_label='PRICE', height=400, title= f"Data Set 5 - {dataset5end} -     {date_and_minute_dictionary[dataset5end]}          Correlation  {time_and_correlation_dictionary[dataset5end]}  ")
Data_Set_5.line(I, J, line_width=1, color="darkorange", alpha=1)
ticks = [0,1, dataset5end]
Data_Set_5.xaxis[0].ticker = ticks
Data_Set_5.xgrid[0].ticker = ticks
Data_Set_5.xgrid.band_fill_alpha  = 0.1
Data_Set_5.xgrid.band_fill_color = "navy"

renderer = Data_Set_5.multi_line([[dataset5start, dataset5start+1]], [[J[0], J[1]]], line_width=5, alpha=0.4, color='red')
draw_tool = FreehandDrawTool(renderers=[renderer], num_objects=10)
Data_Set_5.add_tools(draw_tool)
Data_Set_5.toolbar.active_drag = draw_tool

Data_Set_6 = figure(tools=TOOLS, width=600, x_axis_label='TIME', y_axis_label='PRICE',  height=400, title= f"Data Set 6 - {dataset6end} -     {date_and_minute_dictionary[dataset6end]}          Correlation  {time_and_correlation_dictionary[dataset6end]}  ")
Data_Set_6.line(K, L, line_width=1, color="darkviolet", alpha=1)
ticks = [0,1, dataset6end]
Data_Set_6.xaxis[0].ticker = ticks
Data_Set_6.xgrid[0].ticker = ticks
Data_Set_6.xgrid.band_fill_alpha  = 0.1
Data_Set_6.xgrid.band_fill_color = "navy"

renderer = Data_Set_6.multi_line([[dataset6start, dataset6start+1]], [[L[0], L[1]]], line_width=5, alpha=0.4, color='red')
draw_tool = FreehandDrawTool(renderers=[renderer], num_objects=10)
Data_Set_6.add_tools(draw_tool)
Data_Set_6.toolbar.active_drag = draw_tool

Data_Set_7 = figure(tools=TOOLS, width=600, x_axis_label='TIME', y_axis_label='PRICE', height=400, title= f"Data Set 7 - {dataset7end} -     {date_and_minute_dictionary[dataset7end]}          Correlation  {time_and_correlation_dictionary[dataset7end]}  ")
Data_Set_7.line(M, N, line_width=1, color="blue", alpha=1)
ticks = [0,1, dataset7end]
Data_Set_7.xaxis[0].ticker = ticks
Data_Set_7.xgrid[0].ticker = ticks
Data_Set_7.xgrid.band_fill_alpha  = 0.1
Data_Set_7.xgrid.band_fill_color = "navy"

renderer = Data_Set_7.multi_line([[dataset7start, dataset7start+1]], [[N[0], N[1]]], line_width=5, alpha=0.4, color='red')
draw_tool = FreehandDrawTool(renderers=[renderer], num_objects=10)
Data_Set_7.add_tools(draw_tool)
Data_Set_7.toolbar.active_drag = draw_tool

Data_Set_8 = figure(tools=TOOLS, width=600, x_axis_label='TIME', y_axis_label='PRICE', height=400, title= f"Data Set 8 - {dataset8end} -     {date_and_minute_dictionary[dataset8end]}          Correlation  {time_and_correlation_dictionary[dataset8end]}  ")
Data_Set_8.line(O, P, line_width=1, color="red", alpha=1)
ticks = [0,1, dataset8end]
Data_Set_8.xaxis[0].ticker = ticks
Data_Set_8.xgrid[0].ticker = ticks
Data_Set_8.xgrid.band_fill_alpha  = 0.1
Data_Set_8.xgrid.band_fill_color = "navy"

renderer = Data_Set_8.multi_line([[dataset8start, dataset8start+1]], [[P[0], P[1]]], line_width=5, alpha=0.4, color='red')
draw_tool = FreehandDrawTool(renderers=[renderer], num_objects=10)
Data_Set_8.add_tools(draw_tool)
Data_Set_8.toolbar.active_drag = draw_tool

# put all the plots in a grid layout
p = gridplot( [[Sample_Data, Data_Set_1, Data_Set_2], [Data_Set_3, Data_Set_4, Data_Set_5], [Data_Set_6, Data_Set_7, Data_Set_8]] )

# show the results
show(p)
