import pandas as pd
from itertools import zip_longest
from itertools import chain
import matplotlib.pyplot as plt
import scipy.stats as stats
import numpy as np
import csv

symbol = (input("Which time symbol/coin?  Enter here: "))
suffix = '-1d-data.csv'
combine = symbol + suffix

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


time_cleaned =list(range(1,len(Doc)))    
time_cleaned[-1]


lookback_period = int(input("Enter lookback period in days:"))

def convert_to_float(x,y,z):
    for row in x[-lookback_period:]:
        z.append(float(row[y]))

open_price= []
high_price= []
low_price= []
close_price= []

convert_to_float(Doc[1:],1,open_price)
convert_to_float(Doc[1:],2,high_price)
convert_to_float(Doc[1:],3,low_price)
convert_to_float(Doc[1:],4,close_price)

def percentage_change_1 (x,y,z):
    zip_object = zip(x,y)
    for x,y in zip_object:
        z.append(((y-x)/x)*100)

def percentage_change_2 (x,y,z):
    zip_object = zip(x,y)
    for x,y in zip_object:
        z.append(((y-x)/x)*100)
        
def percentage_change_3 (x,y,z):
    zip_object = zip(x,y)
    for x,y in zip_object:
        z.append(((y-x)/x)*100)
        
def percentage_change_4 (x,y,z):
    zip_object = zip(x,y)
    for x,y in zip_object:
        z.append(((y-x)/x)*100)
        
def percentage_change_5 (x,y,z):
    zip_object = zip(x,y)
    for x,y in zip_object:
        z.append(((y-x)/x)*100)
        
open_to_low_percentage = []
open_to_close_percentage = []
open_to_high_percentage = []
low_to_high_percentage = []
low_to_close_percentage = []

percentage_change_1(open_price,low_price, open_to_low_percentage)
percentage_change_2(open_price,close_price, open_to_close_percentage)
percentage_change_3(open_price,high_price, open_to_high_percentage)
percentage_change_4(low_price,high_price, low_to_high_percentage)
percentage_change_5(low_price,close_price, low_to_close_percentage)

open_to_low_percentage_MIN = min(open_to_low_percentage)
open_to_close_percentage_MIN = min(open_to_close_percentage)
open_to_close_percentage_MAX = max(open_to_close_percentage)
open_to_high_percentage_MAX = max(open_to_high_percentage)
low_to_high_percentage_MIN = min(low_to_high_percentage)
low_to_high_percentage_MAX = max(low_to_high_percentage)
low_to_close_percentage_MAX = max(low_to_close_percentage)

master_df = pd.DataFrame(open_price,columns =["open_price"])
master_df ["high_price"] = high_price
master_df ["low_price"] = low_price
master_df ["close_price"] = close_price

master_df ["open_to_low_percentage"] =open_to_low_percentage
master_df ["open_to_close_percentage"] =open_to_close_percentage
master_df ["open_to_high_percentage"] =open_to_high_percentage
master_df ["low_to_close_percentage"] =low_to_close_percentage
master_df ["low_to_high_percentage"] =low_to_high_percentage


pump_dump_df = pd.DataFrame(open_to_low_percentage,columns =["open_to_low_percentage"])
pump_dump_df ["open_to_close_percentage"] =open_to_close_percentage
pump_dump_df ["open_to_high_percentage"] =open_to_high_percentage
pump_dump_df ["low_to_high_percentage"] =low_to_high_percentage
pump_dump_df ["low_to_close_percentage"] =low_to_close_percentage 


# libraries & dataset

import seaborn as sns
import matplotlib.pyplot as plt
# set a grey background (use sns.set_theme() if seaborn version 0.11.0 or above) 
sns.set(style="darkgrid")
df = pump_dump_df
fig, axs = plt.subplots(2, 2, figsize=(18, 7))
slices = int(input("Enter Bin Number (recommended 70):"))

sns.histplot(data=df, bins=slices , x="open_to_low_percentage", kde=True, color="red", ax=axs[0, 0])
sns.histplot(data=df, bins=slices , x="low_to_high_percentage", kde=True, color="blue", ax=axs[0, 1])
sns.histplot(data=df, bins=slices , x="low_to_close_percentage", kde=True, color="green", ax=axs[1, 0])
sns.histplot(data=df, bins=slices , x="open_to_high_percentage", kde=True, color="teal", ax=axs[1, 1])
plt.savefig(f'{symbol} past {lookback_period} days VAR.jpg', dpi=300)
plt.show()




category = master_df.open_to_low_percentage
print(f"Open to low percentage in the past {lookback_period} days is:")
print(f"98th Percentile is {round(category.quantile(0.02),2)}")
print(f"95th Percentile is {round(category.quantile(0.05),2)}")
print(f"90th Percentile is {round(category.quantile(0.10),2)}") 
print(f"80th Percentile is {round(category.quantile(0.20),2)}") 
print(f"70th Percentile is {round(category.quantile(0.30),2)}") 
print(f"60th Percentile is {round(category.quantile(0.40),2)}") 
print(f"50th Percentile is {round(category.quantile(0.50),2)}") 
print(f"Mean is {category.mean()}") 


