##====================================================##
##     Project: SVM gamma
##        File: protractor_markings.py
##      Author: GOTTFRID OLSSON 
##     Created: 2022-12-02
##     Updated: 2022-12-06
##       About: Plot data in a polar plot.
##====================================================##

import matplotlib
import matplotlib.pyplot as plt
import numpy as np


## FUNCTIONS ##

def draw_degree_text(theta, radius, string):
    rotation_angle_degree = radians_to_degrees(theta) + 90
    plt.text(theta, radius, string, rotation=rotation_angle_degree, verticalalignment="center", horizontalalignment="center")


def draw_radial_line(r_max, r_length, theta, color_string='b', linewidth=1):
    angle = 2*[theta]
    radial_line = [r_max, r_max-r_length]
    plt.polar(angle, radial_line, color=color_string, linewidth=linewidth)


def draw_arc_of_circle(r, x_0=0, y_0=0, theta_start=0, theta_end=2*np.pi, number_of_points = 360*4):
    x_linspace = np.linspace(x_0 - r, x_0 + r, number_of_points, endpoint=True)

    y_plus_linspace  = y_0 + np.sqrt(r**2 - (x_linspace-x_0)**2)
    y_minus_linspace = y_0 - np.sqrt(r**2 - (x_linspace-x_0)**2)

    r_1, theta_1 = certesian_to_polar(x_linspace, y_plus_linspace)
    r_2, theta_2 = certesian_to_polar(x_linspace, y_minus_linspace)
    #print(f"theta_start: {theta_start}\ntheta_end: {theta_end}\n")
    #print(f"theta_1 before: {theta_1}\n")
    for index in range(len(theta_1)):
        if theta_1[index] < theta_start or theta_1[index] > theta_end:
            theta_1[index] = float("nan")
    #print(f"theta_1 after: {theta_1}\n")
    for index in range(len(theta_2)):
        if theta_2[index] < theta_start or theta_2[index] > theta_end:
            theta_2[index] = float("nan")

    plt.polar(theta_1, r_1, 'g-', linewidth=1.5)
    plt.polar(theta_2, r_2, 'r-', linewidth=1.5)


def draw_circle(r, x_0=0, y_0=0, number_of_points=360*2):
    x_linspace = np.linspace(x_0 - r, x_0 + r, number_of_points, endpoint=True)

    y_plus_linspace  = y_0 + np.sqrt(r**2 - (x_linspace-x_0)**2)
    y_minus_linspace = y_0 - np.sqrt(r**2 - (x_linspace-x_0)**2)

    r_1, theta_1 = certesian_to_polar(x_linspace, y_plus_linspace)
    r_2, theta_2 = certesian_to_polar(x_linspace, y_minus_linspace)

    plt.polar(theta_1, r_1, 'k-')
    plt.polar(theta_2, r_2, 'k-')



def polar_to_cartesian(r, theta):
    x = r*np.cos(theta)
    y = r*np.sin(theta)

    return (x, y)


def certesian_to_polar(x, y):
    # https://en.wikipedia.org/wiki/Polar_coordinate_system
    r = np.sqrt(x**2 + y**2)
    theta = [0 for i in range(len(x))]

    for index in range(len(x)):
        if y[index] >= 0 and r[index] != 0:
            theta[index] = np.arccos(x[index]/r[index])
        elif y[index] < 0:
            theta[index] = 2*np.pi-np.arccos(x[index]/r[index]) #added +2*np.pi to get theta in range [0, 2*np.pi]
        else:
            print("Warning, r=0 (x=y=0), angle theta for polar coordinates is undefined")
    
    return (r, theta)


def degrees_to_radians(degree):
    return degree*(np.pi/180)


def radians_to_degrees(radians):
    return radians*(180/np.pi)



matplotlib.rcParams.update({
    "text.usetex": False,
    "font.family": "serif", 
    "font.serif" : ["Computer Modern Roman"]
    })
plt.figure(figsize=(10,10)) #15,15
plt.axes(projection = 'polar')


## DEFINE VARIABLES ##
draw_markings = True
export_figure = False

R_LIM_MAX = 510

R_KUGGHJUL_INNER_RADIUS = 498                 # mm, this needs to be checked! TODO [ ]
X_DISPLACEMENT_ROTATION_AXIS_HOLE_CENTER = 15 # mm, relative the plump hole center, this needs to be checked! TODO [ ]
Y_DISPLACEMENT_ROTATION_AXIS_HOLE_CENTER = -15 # mm, relative the plump hole center, this needs to be checked! TODO [ ]


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

if draw_markings:
    ## 10 DEGREE LINES ##
    for angle_number in range(NUMBER_OF_TEN_MARKINGS):
        theta = degrees_to_radians(THETA_START_DEGREE + angle_number*10)
        r_length = L_TEN_MARKINGS

        draw_radial_line(R_MAX, r_length, theta)
        draw_degree_text(theta, R_MAX-r_length-TEXT_DISTANCE_FROM_MARKINGS, angle_number*10)


    ## 5 DEGREE LINES ##
    for angle_number in range(NUMBER_OF_FIVE_MARKINGS):
        theta = degrees_to_radians(THETA_START_DEGREE + angle_number*5)
        r_length = L_FIVE_MARKINGS

        if (angle_number*5 % 10) != 0: #do not draw TEN_MARKINGS lines again
            draw_radial_line(R_MAX, r_length, theta)
            draw_degree_text(theta, R_MAX-r_length-TEXT_DISTANCE_FROM_MARKINGS, angle_number*5)


    ## 1 DEGREE LINES ##
    for angle_number in range(NUMBER_OF_ONE_MARKINGS):
        theta = degrees_to_radians(THETA_START_DEGREE + angle_number*1)
        r_length = L_ONE_MARKINGS

        if (angle_number % 10) != 0 and (angle_number % 5) != 0: #do not draw TEN_MARKINGS or FIVE_MARKINGS lines again
            draw_radial_line(R_MAX, r_length, theta)


    ## 0.1 DEGREE LINES ##
    for angle_number in range(NUMBER_OF_SUB_ONE_MARKINGS):
        theta = degrees_to_radians(THETA_START_DEGREE + angle_number*0.2)
        r_length = L_SUB_ONE_MARKINGS

        if (angle_number % 10) != 0 and (angle_number % 5) != 0:
            draw_radial_line(R_MAX, r_length, theta)



Delta_theta_axis_radius_circle_left = abs(np.arctan(Y_DISPLACEMENT_ROTATION_AXIS_HOLE_CENTER/R_KUGGHJUL_INNER_RADIUS))
Delta_theta_axis_radius_circle_down = abs(np.arctan(X_DISPLACEMENT_ROTATION_AXIS_HOLE_CENTER/R_KUGGHJUL_INNER_RADIUS))


draw_circle(r=3, x_0=0, y_0=0) #plumb hole
draw_circle(r=18, x_0=X_DISPLACEMENT_ROTATION_AXIS_HOLE_CENTER,
                  y_0=Y_DISPLACEMENT_ROTATION_AXIS_HOLE_CENTER)
draw_arc_of_circle( r=R_KUGGHJUL_INNER_RADIUS,
                    x_0=X_DISPLACEMENT_ROTATION_AXIS_HOLE_CENTER,
                    y_0=Y_DISPLACEMENT_ROTATION_AXIS_HOLE_CENTER,
                    theta_start = np.pi - Delta_theta_axis_radius_circle_left,
                    theta_end = 3*np.pi/2 + Delta_theta_axis_radius_circle_down)

# this works

#TODO: shift the radial lines with (r,theta) --> (x,y), then shift in x,y based on some math i will do, then (x,y) --> (r, theta), plot those



## SET NICE PLOT PROPERTIES ##

ax=plt.gca()
ax.set_rticks([R_MAX, 0])
ax.set_xticks([]) # theta ticks
#ax.set_thetalim(degrees_to_radians(THETA_START_DEGREE), degrees_to_radians(THETA_END_DEGREE))
ax.set_rlim(0, R_LIM_MAX)
if export_figure:
    matplotlib.pyplot.savefig("SVM_g_protractor_lines.pdf", format='pdf', bbox_inches='tight')
plt.show()