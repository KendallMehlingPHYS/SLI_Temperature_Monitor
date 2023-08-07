import base64
from io import BytesIO
from flask import Flask, render_template_string
from matplotlib.figure import Figure
import numpy as np
import datetime
import json
import os
from datetime import date

def get_temp_avg(temp_array):
    avg = round(sum(temp_array)/len(temp_array),2)
    return(avg)
    
def get_temp_std(temp_array):
    std = np.std(temp_array)
    return(std)

# Data part
## Formating date
datetime_fmt = '%Y.%m.%d'
def date_to_mjd(date_string):
    # convert from 'YYYY.MM.DD' date to MJD
    
    dt = datetime.datetime.strptime(date_string, datetime_fmt)
    
    JD = dt.toordinal() + 1721424.5 # convert to julian date (JD)
    MJD = JD - 2400000.5 # convert to modified JD (MJD)
    
    today = int(MJD) # rounding to the integer day
    
    return str(today)


# Flask app
app = Flask(__name__)

@app.route("/")
def index():
    return render_template_string('''
        <html>
        <title>SLI Temperature Monitor</title> 
            <head>
                <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
                <script>
                    $(document).ready(function() {
                        setInterval(function() {
                            var width = $(window).width();
                            var height = $(window).height();
                            $.ajax({
                                url: "/plot?width=" + width + "&height=" + height,
                                success: function(data) {
                                    $('#plot').attr('src', 'data:image/png;base64,' + data);
                                }
                            });
                        }, 5000);
                    });
                </script>
            </head>
            <body>
                <img id="plot" src="" />
            </body>
        </html>
    ''')

@app.route("/plot")
def plot():

        # get the data path. 
    today = date_to_mjd(datetime.datetime.today().strftime(datetime_fmt))
    file_path = os.path.dirname(__file__)   
    file_keithley_1 = os.path.join(file_path, "..", 'Logging/keithley1/'+today+'.txt')
    file_keithley_2 = os.path.join(file_path, "..", 'Logging/keithley2/'+today+'.txt')

    channel_names_1 = ["Temp1", "Temp2", "Temp3", "Temp4", "Temp5", "Temp6",
                       "Temp7", "Temp8"]

    #file_name = "Logging/Arduino/SLI_Temperature_Data{}.txt".format(date.today())
    file_name = "Logging/Arduino/SLI_Temperature_Data2023-08-06.txt"             
    # function for loading data in from the temp file
    def load_temps(path):
        
        # read data in, each entry is a JSON dict, so we read in a list of JSON dicts
        data_load = []
        f = open(file_name)
        data_load = json.load(f)
        #print(data_load)
        hourconv = 1/(60*60)
        # Extract timestamps
        times = [round(hourconv*time,2) for time in np.transpose(data_load["000"][0])]
        #print(times)
        #print(data_load.keys())
        #print(times[-10:])
        
        # Extract temperatures
        temp = [data_load[add][1] for add in data_load.keys()]
        #print(temp)
        temps = {add: [list(temp[0:][ind])] for ind, add in enumerate(channel_names_1)}
       # temps = {address: 1 for address in data_load.keys() }
        #print(temps)
        #print(times)
        return times, temps


    # color scheme
    # Blue box
    colors = {'Temp1': 'black', 'Temp2': 'darkgrey', 'Temp3': 'maroon', 'Temp4': 'sienna',
              'Temp5': 'olive', 'Temp6': 'darkolivegreen', 'Temp7': 'springgreen', 'Temp8': 'deepskyblue'}



    #Load data and prep time window
    times_1, temps_1 = load_temps(file_name)
    # use_all_data = 'no'
    if len(temps_1["Temp1"]) < 40:
        time_window= len(temps_1["Temp1"]) # uses all the data
    else:
        time_window = 40 # change this parameter to look at different time windows relative to the most recent point 

    # Main plot
    # Generate the figure **without using pyplot**.
    fig = Figure(figsize=(18, 10))
    axes = fig.subplots(3, 3)
    # Blues
    axes[0,0].clear()
    axes[0, 0].plot((times_1)[-time_window:], temps_1['Temp1'][-time_window:], '.', label='Temp1', color=colors['Temp1'])
    axes[0, 0].grid()
    axes[0,0].set_ylim([0,25])
    axes[0, 0].legend(loc = "upper right", frameon=False)
    
    
    axes[0, 1].plot((times_1)[-time_window:], temps_1['Temp2'][-time_window:], '.', label='Temp2', color=colors['Temp2'])
    axes[0, 1].grid()
    axes[0, 1].legend()
    
    
    axes[0, 2].plot((times_1)[-time_window:], temps_1['Temp3'][-time_window:], '.', label='Temp3', color=colors['Temp3'])
    axes[0, 2].grid()
    axes[0, 2].legend()
    
    
    axes[1, 0].plot((times_1)[-time_window:], temps_1['Temp4'][-time_window:], '.', label='Temp4', color=colors['Temp4'])
    axes[1, 0].grid()
    axes[1, 0].legend()
    
    
    axes[1, 1].clear()
    axes[1, 1].plot((times_1)[-time_window:], temps_1['Temp5'][-time_window:], '.', label='Temp5', color=colors['Temp5'])
    axes[1, 1].grid()
    axes[1, 1].legend()
    
    
    axes[1, 2].clear()
    axes[1, 2].plot((times_1)[-time_window:], temps_1['Temp6'][-time_window:], '.', label='Temp6', color=colors['Temp6'])
    axes[1, 2].grid()
    axes[1, 2].legend()
    
    
    
    axes[2, 0].clear()
    axes[2, 0].plot((times_1)[-time_window:], temps_1['Temp7'][-time_window:], '.', label='Temp7', color=colors['Temp7'])
    axes[2, 0].grid()
    axes[2, 0].legend()
    
    
    
    axes[2, 1].clear()
    axes[2, 1].plot((times_1)[-time_window:], temps_1['Temp8'][-time_window:], '.', label='Temp8', color=colors['Temp8'])
    axes[2, 1].grid()
    axes[2, 1].legend()
    
    
    # axes[0, 0].plot((times_1 - times_1[0])[-time_window:]*24., temps_1['blue master'][-time_window:], '.', label='Blue Master', color=colors['Blue Master'])
    # axes[0, 0].plot((times_1 - times_1[0])[-time_window:]*24., temps_1['injection fiber'][-time_window:], '.', label='Injection Fiber', color=colors['Injection Fiber'])
    # axes[0, 0].set(ylabel='Temperature (C)', xlabel='Time (Hours)', title="Blue table")
    # axes[0, 0].grid()
    # axes[0, 0].legend()


    # # Red and lattice laser table 
    # axes[0, 1].clear()
    # thermistors = [16,31,32,33]
    # for i in thermistors:
    #     axes[0, 1].plot((times_2 - times_2[0])[-time_window:]*24., temps_2[channel_names_2[i]][-time_window:],
    #             '.', label=channel_names_2[i], color=colors[channel_names_2[i]])
    # axes[0, 1].set(ylabel='Temperature (C)', xlabel='Time (Hours)', title='689 and 813 table')
    # axes[0, 1].legend()
    # axes[0, 1].grid()

    # # Main chamber
    # thermistors = [6,7,14,15,17,18,19,10,25,26,27,28,29,30,34]#15#,31,32,33]
    # axes[0, 2].clear()
    # for i in thermistors:
    #     axes[0, 2].plot((times_2 - times_2[0])[-time_window:]*24., temps_2[channel_names_2[i]][-time_window:], '.', label=channel_names_2[i], color=colors[channel_names_2[i]])
    # axes[0, 2].set(ylabel='Temperature (C)', xlabel='Time (Hours)', title='Main chamber')
    # axes[0, 2].legend(fontsize="small", ncol=3)
    # axes[0, 2].grid()

    # #  View ports 
    # axes[1, 0].clear()
    # thermistors = [0,5,8,10,12,21,23,36]
    # for i in thermistors:
    #     axes[1, 0].plot((times_2 - times_2[0])[-time_window:]*24., temps_2[channel_names_2[i]][-time_window:], '.', label=channel_names_2[i], color=colors[channel_names_2[i]])
    # axes[1, 0].set(ylabel='Temperature (C)', xlabel='Time (Hours)', title='Chamber viewports')
    # axes[1, 0].grid()
    # axes[1, 0].legend()

    # # MOT coils
    # axes[1, 1].clear()
    # thermistors = [2,3]
    # for i in thermistors:
    #     axes[1, 1].plot((times_2 - times_2[0])[-time_window:]*24., temps_2[channel_names_2[i]][-time_window:], '.', label=channel_names_2[i])
    # axes[1, 1].set(ylabel='Temperature (C)', xlabel='Time (Hours)', title='MOT coils')
    # axes[1, 1].grid()
    # axes[1, 1].legend()

    # Notes 
    axes[-1, -1].clear()
    axes[-1, -1].annotate(
        "Today: "+str(datetime.datetime.today().strftime(datetime_fmt))+
        "\n last update: {}".format(str(datetime.datetime.now())) +
        "\n - x-axis starts from 0:00 a.m."+
        "\n - For the close-up, go J/notebooks/[date]/plot_temps.ipynb",
        (0, 0.5))
    axes[-1, -1].axis("off")

    fig.suptitle("Sr1 live temperature monitor")
    # fig.tight_layout()

    # Save it to a temporary buffer.
    buf = BytesIO()
    fig.savefig(buf, format="png")
    # Embed the result in the html output.
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return data

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000)
