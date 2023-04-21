##====================================================##
##     Project: SVM analysis curvefit
##        File: curvefit.py
##      Author: GOTTFRID OLSSON 
##     Created: 2022-12-11
##     Updated: 2022-12-11
##       About: Plot measured data for one day 
##              and fitted curve.
##====================================================##


import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from scipy.optimize import curve_fit
from datetime import datetime


matplotlib.rcParams.update({
    "text.usetex": True,
    "font.family": "serif", 
    "font.serif" : ["Computer Modern Roman"], 
    "font.size"  : 11,
    "figure.figsize" : (16/2.54, 9/2.54)
})
matplotlib.rc('font',   size=11)      #2022-06-21: not sure what the difference is, to test later on!
matplotlib.rc('axes',   titlesize=11) #2022-06-21: not sure what the difference is, to test later on!
matplotlib.rc('axes',   labelsize=11) #2022-06-21: not sure what the difference is, to test later on!
matplotlib.rc('xtick',  labelsize=9)
matplotlib.rc('ytick',  labelsize=9)
matplotlib.rc('legend', fontsize=9)


day = "2022-06-05"
measured_angle_degree = [54.25, 37.25, 36.75, 36.25, 36.00, 35.50, 35.25, 35.00, 35.00, 35.00, 35.25, 35.25, 35.50, 35.75, 36.25, 36.75, 37.25, 43.25]
measured_angle_uncertainty_degree = [0.25 for i in measured_angle_degree]
time_of_day           = ["09:15", "12:00", "12:10", "12:20", "12:30", "12:40", "12:50", "13:00", "13:10", "13:20", "13:30", "13:40", "13:50", "14:00", "14:10", "14:20", "14:30", "15:28"]
minutes_from_midnight = []

measured_angle_degree = measured_angle_degree[1:-1]
measured_angle_uncertainty_degree = [0.25 for i in measured_angle_degree]
time_of_day           = time_of_day[1:-1]


def get_minutes_from_midnight_from_time_of_day(time_of_day_string, time_of_day_dattime_format="%H:%M"):
        time = datetime.strptime(time_of_day_string, time_of_day_dattime_format)

        hours = time.hour
        minutes = time.minute

        minutes_from_midnight = hours*60 + minutes

        return minutes_from_midnight

def cosinus_fit_function(x, a, b, c, d):
        return a + b*np.cos(c*x + d)


for i, time in enumerate(time_of_day): minutes_from_midnight.append( get_minutes_from_midnight_from_time_of_day(time) )
minutes_from_midnight_linspace = np.linspace(0, 23*60+59, 15*(23*60+59+1))


# 4. fit cos-curve to measured data
initial_parameter_guess = [60, 25, 0.01, 0] #guessed (first and second value should be (sort of) latitude and earths axial tilt, respectively)
fit_parameters, fit_parameters_covariance = curve_fit(cosinus_fit_function, minutes_from_midnight, measured_angle_degree, p0=initial_parameter_guess)

a, b, c, d = fit_parameters[0], fit_parameters[1], fit_parameters[2], fit_parameters[3]
a, b, c, d = np.array(a), np.array(b), np.array(c), np.array(d) #to make np.cos(*args) stop crying
print(a, b, c, d)
fitted_curve_values = a + b*np.cos(c*(minutes_from_midnight_linspace) + d)


minumum_angle_fitted_curve = np.min(fitted_curve_values)
minute_at_minimum_angle_fitted_curve = 99999

for index, minute in enumerate(minutes_from_midnight_linspace):
        if minute >= np.min(minutes_from_midnight) and minute <= np.max(minutes_from_midnight):
                if fitted_curve_values[index] < fitted_curve_values[index-1]:
                        minute_at_minimum_angle_fitted_curve = minutes_from_midnight_linspace[index]

#print(minute_at_minimum_angle_fitted_curve, minumum_angle_fitted_curve)

## PLOT ##
minute_buffer_plot = 30
angle_buffer_plot = 0.5
#plt.title(f"Measurement on {day}\nFitted curve: {a:.1f}+{b:.1f}cos({c:.2f}x+{d:.2f})")
fig, ax = plt.subplots(1, 1, figsize=((16/2.54, 9/2.54)))

ax.errorbar(x=minutes_from_midnight, y=measured_angle_degree, yerr=measured_angle_uncertainty_degree, color='r', linestyle='', linewidth=1.62, marker='o', markersize=5, markerfacecolor="None", markeredgewidth=1.62, label='Mätvärden', elinewidth=1.62, capsize=3, barsabove=0)
ax.plot(minutes_from_midnight_linspace, fitted_curve_values, 'k--', linewidth=1.62, label=f"Anpassad cosinuskurva\n${a:.2f}+{b:.2f}cos({c:.2f}x+{d:.2f})$")
#plt.plot(minute_at_minimum_angle_fitted_curve, minumum_angle_fitted_curve, 'bo', label=f': {minumum_angle_fitted_curve:.2f}')

#plt.xlim(np.min(minutes_from_midnight)-minute_buffer_plot, np.max(minutes_from_midnight)+minute_buffer_plot)
plt.xlim(700, 900)
#plt.ylim(np.min(measured_angle_degree)-angle_buffer_plot,  np.max(measured_angle_degree)+angle_buffer_plot)
plt.ylim(34.5, 38)
plt.xlabel(f"Tid på dagen {day} från 00:00 (min)")
plt.ylabel(f"Vinkel $\\beta$ (grader)")


yFormatString = '{:.1f}'
ax.get_yaxis().set_major_formatter( matplotlib.ticker.FuncFormatter(lambda x, pos: yFormatString.format(x).replace('.', ',')) ) 


plt.grid()
plt.legend(loc='upper center')
plt.tight_layout()
plt.savefig(f"Beta_funktion_tid_dag_{day}.pdf")
plt.show()