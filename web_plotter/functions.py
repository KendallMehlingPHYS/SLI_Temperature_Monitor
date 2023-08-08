import numpy as np


def get_temp_avg(temp_array):
    avg = round(sum(temp_array)/len(temp_array),2)
    return(avg)
    
def get_temp_std(temp_array):
    std = round(np.std(temp_array, dtype=np.float64),1)
    return(std)




