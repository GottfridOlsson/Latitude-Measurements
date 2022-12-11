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
from scipy.optimize import curve_fit
from datetime import datetime



day = "2022-12-11"
measured_angle_degree = [80.75, 80.50, 80.50, 80.75, 80.75, 81.25, 82.00]
time_of_day           = ["11:35", "11:50", "12:05", "12:20", "12:35", "12:50", "13:23"]
minutes_from_midnight = []



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

fitted_curve_values = a + b*np.cos(c*(minutes_from_midnight_linspace) + d)


minumum_angle_fitted_curve = np.min(fitted_curve_values)
minute_at_minimum_angle_fitted_curve = 99999

for index, minute in enumerate(minutes_from_midnight_linspace):
        if minute >= np.min(minutes_from_midnight) and minute <= np.max(minutes_from_midnight):
                if fitted_curve_values[index] < fitted_curve_values[index-1]:
                        minute_at_minimum_angle_fitted_curve = minutes_from_midnight_linspace[index]

print(minute_at_minimum_angle_fitted_curve, minumum_angle_fitted_curve)

## PLOT ##
minute_buffer_plot = 30
angle_buffer_plot = 0.5
plt.title(f"Measurement on {day}\nFitted curve: {a:.1f}+{b:.1f}cos({c:.2f}x+{d:.2f})")

plt.plot(minutes_from_midnight, measured_angle_degree, 'rx', label='Measured angle')
plt.plot(minutes_from_midnight_linspace, fitted_curve_values, 'k--', label='Fitted curve')
plt.plot(minute_at_minimum_angle_fitted_curve, minumum_angle_fitted_curve, 'bo', label=f'Minimum angle from fit: {minumum_angle_fitted_curve:.2f}')

plt.xlim(np.min(minutes_from_midnight)-minute_buffer_plot, np.max(minutes_from_midnight)+minute_buffer_plot)
plt.ylim(np.min(measured_angle_degree)-angle_buffer_plot,  np.max(measured_angle_degree)+angle_buffer_plot)
plt.legend()
plt.show()