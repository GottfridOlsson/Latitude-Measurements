import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# FUNCTIONS #
def CSV_read_file(readFilePath):
        CSV =  pd.read_csv(readFilePath, sep=",")
        return CSV

def CSV_get_header(CSV_data):
        return CSV_data.columns.values

def write_DataFrame_to_CSV(DataFrame, write_file_path):
        DataFrame.to_csv(write_file_path, sep=",", encoding='utf-8', index=False)

def convert_list_of_lists_and_header_to_DataFrame(list_of_lists, header):
        dataframe = pd.DataFrame(list_of_lists).transpose()
        dataframe.columns = header
        return dataframe

def cosinus_fit_function(x, a, b, c, d):
        return a + b*np.cos((2*np.pi/c)*(x + d))


# Read input data #
CSV_input = CSV_read_file("Formatted CSV\SVM_PlotData_from_2022-01-01_to_2022-12-31.csv")
header_input = CSV_get_header(CSV_input)

days_from_2022jan1 = CSV_input[header_input[0]] 
days_measured_beta = CSV_input[header_input[3]]
measured_beta     = CSV_input[header_input[4]] #naive min
uncertainty_beta  = CSV_input[header_input[5]]

x = days_from_2022jan1
x_to_fit = days_measured_beta[~np.isnan(days_measured_beta)] #removes NaN
y_to_fit = measured_beta[~np.isnan(measured_beta)] #removes NaN

x = x - np.ones_like(x)*365
x_to_fit = x_to_fit - np.ones_like(x_to_fit)*365


# Fit cosinus: Least squares (MK) #
fit_parameters_MK, fit_parameters_covariance_MK = curve_fit(cosinus_fit_function, x_to_fit, y_to_fit, p0=[23, 57, 365, 10])
one_sigma_MK = np.sqrt(np.diag(fit_parameters_covariance_MK))

a_MK, b_MK, c_MK, d_MK = fit_parameters_MK[0], fit_parameters_MK[1], fit_parameters_MK[2], fit_parameters_MK[3]
a_MK, b_MK, c_MK, d_MK = np.array(a_MK), np.array(b_MK), np.array(c_MK), np.array(d_MK) #to make np.cos(*args) stop crying
print(a_MK, b_MK, c_MK, d_MK, one_sigma_MK)

# Fit cosinus: Bayesian analysis (BA) #
a_BA, b_BA, c_BA, d_BA = 57.743, 23.495, 372.719, 16.117
plt.plot(x, cosinus_fit_function(x, a_BA, b_BA, c_BA, d_BA), 'b', label=f"BA: {a_BA:.2f} + {b_BA:.2f}cos(2pi/{c_BA:.2f}(x+{d_BA:.2f}))")
plt.plot(x, cosinus_fit_function(x, a_MK, b_MK, c_MK, d_MK), 'k--', label=f"MK: {a_MK:.2f} + {b_MK:.2f}cos(2pi/{c_MK:.2f}(x+{d_MK:.2f}))")
plt.plot(x_to_fit, y_to_fit, 'ro', label='Measured')
plt.plot(x, cosinus_fit_function(x, 57.68, 23.44, 365.24, 10), label='Simple model')
plt.legend()
plt.show()


EXPORT_DATA_TO_CSV = True
# 5. export data to CSV (s.t. it can be plotted with PlotData.py)
if EXPORT_DATA_TO_CSV:
        all_days           = x 
        fitted_MK_curve    = cosinus_fit_function(x, a_MK, b_MK, c_MK, d_MK)
        fitted_BA_curve    = cosinus_fit_function(x, a_BA, b_BA, c_BA, d_BA)
        theoretical_curve  = cosinus_fit_function(x, 57.68, 23.44, 365.24, 10)
        days_measured_beta = x_to_fit
        measured_beta      = measured_beta
        uncertainty_beta   = uncertainty_beta

        data   = [all_days, fitted_MK_curve, fitted_BA_curve, theoretical_curve, days_measured_beta, measured_beta, uncertainty_beta]
        header = ["All days with start 2021-01-01", "Fitted curve MK (deg)", "Fitted curve BA (deg)", "Theoretical curve simple model (deg)", "Days when measured beta", "Beta naive min (deg)", " Beta uncertainty pm (deg)"]

        dataframe = convert_list_of_lists_and_header_to_DataFrame(data, header)

        export_CSV_file_path = "Formatted CSV/SVM_PlotData_Beta_MK_BA_fits_simple_model_curve_2023-04-16.csv"
        write_DataFrame_to_CSV(dataframe, export_CSV_file_path)
