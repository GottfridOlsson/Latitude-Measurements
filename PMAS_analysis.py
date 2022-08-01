##====================================================##
##     Project: PMAS analysis
##        File: PMAS_analysis.py
##      Author: GOTTFRID OLSSON 
##     Created: 2022-08-01, 16:16
##     Updated: 2022-08-01, 17:56
##       About: Plot measured data and fitted curve.
##====================================================##



## IMPORTS ##

from sqlite3 import DateFromTicks
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from datetime import datetime


## CONSTANTS ##

CSV_DELIMITER = ','
CSV_PATH = 'PMAS Latitude Measurements [2022-08-01].csv'

LATITUDE_DOKTOR_FORSELIUS_BACKE_50_GBG_GOOGLEMAPS = 57.6786 #degree north

START_DATE = "2021-01-01" #first_date: 2021-02-27;  PMAS v. beta from: 2022-01-06;  PMAS v. beta (more accurate?) from: 2022-04-18
END_DATE   = "2022-08-01"


## FUNCTIONS ##


# --- CSV --- #

def CSV_read_file(readFilePath):
    print("In progress: Reading CSV " + readFilePath)
    CSV =  pd.read_csv(readFilePath, sep=CSV_DELIMITER)
    print("DONE: Reading CSV: " + readFilePath)
    return CSV

def CSV_get_header(CSV_data):
    return CSV_data.columns.values


# --- other --- #

def get_unique_dates(CSV, start_date, end_date):
        header        = CSV_get_header(CSV)
        date_interval = CSV[ (CSV[header[0]] >= start_date) & (CSV[header[0]] <= end_date) ]
        unique_dates  = date_interval.date.drop_duplicates()
        return unique_dates

def get_days_between_date_and_START_DAY(date):
        date_format_ISO8601 = "%Y-%m-%d"
        start = datetime.strptime(START_DATE, date_format_ISO8601)
        end = datetime.strptime(date, date_format_ISO8601)
        delta = end - start
        return delta.days





## MAIN ##

if __name__=='__main__':

        # 1. read CSV

        CSV    = CSV_read_file(CSV_PATH)
        header = CSV_get_header(CSV)

        date        = CSV[header[0]]
        time_of_day = CSV[header[1]] #how do you handle blank space in header? "time_of_day = CSV.time_of_day (hh:mm)" looks very wrong with " " in it. //2022-08-01
        alpha       = CSV[header[2]]
        uncertainty = CSV[header[3]]

        ###print(CSV)


        # 2. select date-range [start_date, end_date] (inclusive) for analysis

        unique_dates  = get_unique_dates(CSV, START_DATE, END_DATE)
        
        alpha_naive_min = []
        alpha_naive_actual_min_check = [] #0 if false (no larger measured angle for the same day), 1 if true (larger, or equal, angle measured the same day)

        for i, day in enumerate(unique_dates):
                #print(i, day, "test")
                angles_of_date = CSV[CSV[header[0]]==day][header[2]] # get value "CSV[*row*][*col*] = CSV[date=day][angle (deg)]"
                alpha_naive_min.append(min(angles_of_date))
                #print(angles_of_date, alpha_naive_min)
                alpha_naive_actual_min_check.append(0)
                
                #for j, alpha in enumerate(angles_of_date):     
                #        if j >= 1: # and angles_of_date[j] >= angles_of_date[j-1]:
                #                print("j_min: " + str(angles_of_date[j]))
                #                #print(angles_of_date[j-1])
                #                alpha_naive_actual_min_check[-1] = 1

        
        print("the end \n", alpha_naive_min)
        print(alpha_naive_actual_min_check)
 
        print(get_days_between_date_and_START_DAY("2021-01-02")) #seems to be working! //2022-08-01

        # 3. get naive (!) minimal angle (alpha) for each unique date (improvement: do a cos-fit to measured alpha for each date to find a more precise minimal angle)
        min_angle = []

                # 3b. only include naive minimal angles which have higher valued angle at later time the same date (otherwise we cannot be sure it is a minima)


        # 4. fit cos-curve to measured data

### to plot: need to convert unique_days from dates to number of days (whole days) with start (=0) START_DATE and end at END_DATE (calc. all days in between)
        # 5. plot fit and data points and fitted curve and compare with theoretical curve 
       # plt.plot(unique_dates, alpha_naive_min, markerSize=5, marker="x", lineWidth=0)
       # plt.show()
        # 


        #print(date, time_of_day, alpha, uncertainty)

