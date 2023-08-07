import serial
import numpy as np
import json
import os
from datetime import date, datetime


data_path = os.getcwd() + "\Logging\Arduino"
file_path = data_path + '\\SLI_Temperature_Data2023-08-03'
#file_path = data_path + "\SLI_Temperature_Data" + str(date.today())
print(file_path)
def load_temps(channels):
    
    # read data in, each entry is a JSON dict, so we read in a list of JSON dicts 
    f = open (file_path + '.json', "r")
    data_load = json.loads(f.read())
    keys = data_load.keys()
    times = np.transpose([data_load[key][0][0] for key in data_load.keys()])
    temp = np.transpose([data_load[key][1][1] for key in data_load.keys()])
    if len(data_load[list(keys)[0]]) < 40:
        window = len(data_load[list(keys)[0]])
    else:
        window = 40
    print(window)
    temps = {channels[entry]: temp[entry] for entry in range(len(channels))}   
    # # Extract temperatures

 
    
    return times, temps
channels = ["Temp1", "Temp2", "Temp3", "Temp4", "Temp5", "Temp6", "Temp7", "Temp8"]

otimes, otemps = load_temps(channels)

print(otimes)
print(otemps)