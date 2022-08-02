##====================================================##
##     Project: PMAS analysis
##        File: PMAS_analysis.py
##      Author: GOTTFRID OLSSON 
##     Created: 2022-08-01, 16:16
##     Updated: 2022-08-02, 08:19
##       About: Plot measured data and fitted curve.
##====================================================##



## IMPORTS ##

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from scipy.optimize import curve_fit



## CONSTANTS ##

CSV_DELIMITER = ','
CSV_PATH = 'PMAS Latitude Measurements [2022-08-01].csv'

LATITUDE_DOKTOR_FORSELIUS_BACKE_50_GBG = 57.6786 #degree north, Google Maps
EARTHS_AXIAL_TILT = 23.44; # degrees, https://nssdc.gsfc.nasa.gov/planetary/factsheet/earthfact.html

START_DATE = "2021-01-01" #first_date: 2021-02-27;  PMAS v. beta from: 2022-01-06;  PMAS v. beta (more accurate?) from: 2022-04-18
END_DATE   = "2022-08-01"
EXTRA_DAYS_PLOT = 20


## FUNCTIONS ##


# --- CSV --- #

def CSV_read_file(readFilePath):
    CSV =  pd.read_csv(readFilePath, sep=CSV_DELIMITER)
    return CSV

def CSV_get_header(CSV_data):
    return CSV_data.columns.values


# --- other --- #

def get_unique_dates(CSV, start_date, end_date):
        header        = CSV_get_header(CSV)
        date_interval = CSV[ (CSV[header[0]] >= start_date) & (CSV[header[0]] <= end_date) ]
        unique_dates  = date_interval.date.drop_duplicates()
        return unique_dates

def get_days_between_date_and_START_DATE(date):
        date_format_ISO8601 = "%Y-%m-%d"
        start = datetime.strptime(START_DATE, date_format_ISO8601)
        end   = datetime.strptime(date, date_format_ISO8601)
        delta = end - start
        return delta.days

def cosinus_fit_function(x, a, b, c, d):
        return a + b*np.cos(c*x + d)

def theoretical_correction_curve(day_of_year):
        return -EARTHS_AXIAL_TILT*np.cos(2*np.pi*(day_of_year+10)/365)


## MAIN ##

if __name__=='__main__':

        # 1. read data from CSV

        CSV    = CSV_read_file(CSV_PATH)
        header = CSV_get_header(CSV)

        date        = CSV[header[0]]
        time_of_day = CSV[header[1]]
        alpha       = CSV[header[2]]
        uncertainty = CSV[header[3]]



        # 2. select date-range [start_date, end_date] (inclusive) for analysis

        unique_dates = get_unique_dates(CSV, START_DATE, END_DATE)
        


        # 3. get naive (!) minimal angle (alpha) for each unique date (IMPROVEMENT: do a cosinus-fit to measured alpha for each date to find a more precise minimal angle)
        
        alpha_naive_min = []
        alpha_naive_actual_min_check = [] #0 if false (no larger measured angle for the same day), 1 if true (larger, or equal, angle measured the same day)
        days_between_unique_dates_and_START_DATE = []
        

        for i, date in enumerate(unique_dates):
                angles_of_date = CSV[CSV[header[0]]==date][header[2]] # get value "CSV[*row*][*col*] = CSV[date=day][angle (deg)]"
                
                alpha_naive_min.append(min(angles_of_date))
                alpha_naive_actual_min_check.append(0)
                days_between_unique_dates_and_START_DATE.append(get_days_between_date_and_START_DATE(date))

                # if larger measured angle for the same day exists, then naive check is OK = 1
                for j, alpha in enumerate(angles_of_date):     
                        if j >= 1 and angles_of_date.iloc[j] >= angles_of_date.iloc[j-1]:                              
                                alpha_naive_actual_min_check[-1] = 1


        # 3b. only include naive minimal angles which have higher valued angle at later time the same date (otherwise we cannot be sure it is a minima)

        selected_alpha_naive_min = [x for i, x in enumerate(alpha_naive_min) if alpha_naive_actual_min_check[i] == 1]
        selected_days_between_unique_dates_and_START_DATE = [x for i, x in enumerate(days_between_unique_dates_and_START_DATE) if alpha_naive_actual_min_check[i] == 1]
        all_days_between_START_and_END_DATE = [x for x in range(0, get_days_between_date_and_START_DATE(END_DATE)+EXTRA_DAYS_PLOT)]



        # 4. fit cos-curve to measured data
        initial_parameter_guess = [LATITUDE_DOKTOR_FORSELIUS_BACKE_50_GBG, EARTHS_AXIAL_TILT, 2*np.pi/365, 0] #from knowledge of physics/the theoretical equation
        fit_parameters, fit_parameters_covariance = curve_fit(cosinus_fit_function, selected_days_between_unique_dates_and_START_DATE, selected_alpha_naive_min, p0=initial_parameter_guess)

        a, b, c, d = fit_parameters[0], fit_parameters[1], fit_parameters[2], fit_parameters[3]
        a, b, c, d = np.array(a), np.array(b), np.array(c), np.array(d) #to make np.cos(*args) stop crying

        fitted_curve_values = a + b*np.cos(c*all_days_between_START_and_END_DATE + d)
        theoretical_curve_values = LATITUDE_DOKTOR_FORSELIUS_BACKE_50_GBG + EARTHS_AXIAL_TILT*np.cos(2*np.pi*(all_days_between_START_and_END_DATE+np.array(10))/365)
        


        # 5. plot fit and data points and fitted curve and compare with theoretical curve 

        plt.plot(selected_days_between_unique_dates_and_START_DATE, selected_alpha_naive_min, markersize=5, marker="x", linewidth=0, color="#FF0000")
        plt.plot(all_days_between_START_and_END_DATE, theoretical_curve_values, linestyle="--", color="#000000")
        plt.plot(all_days_between_START_and_END_DATE, fitted_curve_values, linestyle="-", color="#0000FF")

        title_fitted = "         Fitted curve: %.2f + %.2f * cos(%.4fx + %.3f)\n" % (a, b, c, d)
        title_theoretical = "Theoretical curve: %.2f + %.2f * cos(%.4fx + %.3f)" % (LATITUDE_DOKTOR_FORSELIUS_BACKE_50_GBG, EARTHS_AXIAL_TILT, 2*np.pi/365, 2*np.pi*10/365)
        plt.title(title_fitted + title_theoretical)
        plt.show()
        plt.legend("Datapoints", "Theoretical", "Fitted")
        


        # 6. print interesting values to compare fit with theoretical
        print("\n\t\tLatitude (deg)\tEarths axial tilt (deg)\tCos day coeff.\tCos shift coeff.\n\t   |    ------------------------------------------------------------------------")
        print("     Fitted|\t%.3f\t\t%.2f\t\t\t%.4f\t\t\t%.4f" % (a,b,c,d))
        print("Theoretical|\t%.3f\t\t%.2f\t\t\t%.4f\t\t\t%.4f" % (LATITUDE_DOKTOR_FORSELIUS_BACKE_50_GBG, EARTHS_AXIAL_TILT, 2*np.pi/365, 2*np.pi*10/365))
        print("\t   |    ------------------------------------------------------------------------")
        print(" Rel. error|\t%.2f %%\t\t%.2f %%\t\t\t%.2f %%\t\t\t%.2f %%" % ((a/LATITUDE_DOKTOR_FORSELIUS_BACKE_50_GBG-1)*100, (b/EARTHS_AXIAL_TILT-1)*100, (c/(2*np.pi/365)-1)*100, (d/(2*np.pi*10/365)-1)*100))


### EOF ###