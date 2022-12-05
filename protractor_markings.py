##====================================================##
##     Project: SVM gamma
##        File: protractor_markings.py
##      Author: GOTTFRID OLSSON 
##     Created: 2022-12-02, 20:43
##     Updated: 2022-12-02, 20:43
##       About: Plot data in a polar plot.
##====================================================##

import matplotlib
import matplotlib.pyplot as plt
import numpy as np


## FUNCTIONS ##

def draw_radial_line(r_max, r_length, theta, color_string='b', linewidth=1):
    angle = 2*[theta]
    radial_line = [r_max, r_max-r_length]
    plt.polar(angle, radial_line, color=color_string, linewidth=linewidth)

def draw_degree_text(theta, radius, string):
    rotation_angle_degree = radians_2_degree(theta) + 90
    plt.text(theta, radius, string, rotation=rotation_angle_degree, verticalalignment="center", horizontalalignment="center")

def degree_2_radians(degree):
    return degree*(np.pi/180)

def radians_2_degree(radians):
    return radians*(180/np.pi)


matplotlib.rcParams.update({
    "text.usetex": True,
    "font.family": "serif", 
    "font.serif" : ["Computer Modern Roman"]
    })
plt.figure(figsize=(15,15))
plt.axes(projection = 'polar')


## DEFINE VARIABLES ##
export_figure = True

R_MAX = 475             # mm, max radius for angle lines
L_TEN_MARKINGS     = 40 # mm, length of lines for the markings
L_FIVE_MARKINGS    = 32 # mm, length of lines for the markings
L_ONE_MARKINGS     = 25 # mm, length of lines for the markings
L_SUB_ONE_MARKINGS = 12 # mm, length of lines for the markings

THETA_START_DEGREE = 180
THETA_END_DEGREE   = 270  

NUMBER_OF_TEN_MARKINGS      = 10
NUMBER_OF_FIVE_MARKINGS     = 10 - 1 + NUMBER_OF_TEN_MARKINGS
NUMBER_OF_ONE_MARKINGS      = 90
NUMBER_OF_SUB_ONE_MARKINGS  = 4 * 90 + NUMBER_OF_ONE_MARKINGS #think: 9 between each whole degree, but draw 4 with lines and use the 5 spaces between lines as implicit markings

TEXT_DISTANCE_FROM_MARKINGS = 5


## SVM gamma PROTRACTOR LINES ##

## 10 DEGREE LINES ##
for angle_number in range(NUMBER_OF_TEN_MARKINGS):
    theta = degree_2_radians(THETA_START_DEGREE + angle_number*10)
    r_length = L_TEN_MARKINGS

    draw_radial_line(R_MAX, r_length, theta)
    draw_degree_text(theta, R_MAX-r_length-TEXT_DISTANCE_FROM_MARKINGS, angle_number*10)


## 5 DEGREE LINES ##
for angle_number in range(NUMBER_OF_FIVE_MARKINGS):
    theta = degree_2_radians(THETA_START_DEGREE + angle_number*5)
    r_length = L_FIVE_MARKINGS

    if (angle_number*5 % 10) != 0: #do not draw TEN_MARKINGS lines again
        draw_radial_line(R_MAX, r_length, theta)
        draw_degree_text(theta, R_MAX-r_length-TEXT_DISTANCE_FROM_MARKINGS, angle_number*5)


## 1 DEGREE LINES ##
for angle_number in range(NUMBER_OF_ONE_MARKINGS):
    theta = degree_2_radians(THETA_START_DEGREE + angle_number*1)
    r_length = L_ONE_MARKINGS

    if (angle_number % 10) != 0 and (angle_number % 5) != 0: #do not draw TEN_MARKINGS or FIVE_MARKINGS lines again
        draw_radial_line(R_MAX, r_length, theta)


## 0.1 DEGREE LINES ##
for angle_number in range(NUMBER_OF_SUB_ONE_MARKINGS):
    theta = degree_2_radians(THETA_START_DEGREE + angle_number*0.2)
    r_length = L_SUB_ONE_MARKINGS

    if (angle_number % 10) != 0 and (angle_number % 5) != 0:
        draw_radial_line(R_MAX, r_length, theta)



## SET NICE PLOT PROPERTIES ##

ax=plt.gca()
ax.set_rticks([R_MAX, 0])
ax.set_xticks([]) # theta ticks
ax.set_thetalim(degree_2_radians(THETA_START_DEGREE), degree_2_radians(THETA_END_DEGREE))
ax.set_rlim(0, R_MAX)
if export_figure:
    f.export_figure_as_pdf("SVM_g_protractor_lines.pdf")
plt.show()