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



def draw_radial_line(r_max, r_length, theta, r_outward_displacement=0, color_string='b', linewidth=1):
    angle = 2*[theta]
    radial_line = [r_max + r_outward_displacement, r_max + r_outward_displacement - r_length]
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

    plt.polar(theta_1, r_1, 'r-', linewidth=1.5)
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
draw_old_markings = False
export_figure = False
export_figure_as_test = True


R_LIM_MAX = 510
R_LIM_MIN = 0

R_KUGGHJUL_INNER_RADIUS = 474                 # mm, //2022-12-08
X_DISPLACEMENT_ROTATION_AXIS_HOLE_CENTER = 29 # mm, relative the plump hole center //2022-12-08
Y_DISPLACEMENT_ROTATION_AXIS_HOLE_CENTER = -21 # mm, relative the plump hole center //2022-12-08

R_AXISHOLE_CIRCLE_RADIUS_AT_THETA_270_DEGREES = X_DISPLACEMENT_ROTATION_AXIS_HOLE_CENTER + R_KUGGHJUL_INNER_RADIUS

R_DISTANCE_BETWEEN_KUGGHJUL_RADIUS_AND_MARKINGS= 15 # mm,
R_MARKINGS_MAX = R_KUGGHJUL_INNER_RADIUS - R_DISTANCE_BETWEEN_KUGGHJUL_RADIUS_AND_MARKINGS             # mm, max radius for angle lines
L_TEN_MARKINGS     = 40 # mm, length of lines for the markings
L_FIVE_MARKINGS    = 32 # mm, length of lines for the markings
L_ONE_MARKINGS     = 25 # mm, length of lines for the markings
L_SUB_ONE_MARKINGS = 12 # mm, length of lines for the markings

R_DIFFERENCE_BETWEEN_KUGGHJUL_RADIUS_AND_MARKINGS_RADIUS_AT_THETA_270_DEGREES = abs(R_AXISHOLE_CIRCLE_RADIUS_AT_THETA_270_DEGREES - R_MARKINGS_MAX)

THETA_START_DEGREE = 180
THETA_END_DEGREE   = 270  

NUMBER_OF_TEN_MARKINGS      = 10
NUMBER_OF_FIVE_MARKINGS     = 10 - 1 + NUMBER_OF_TEN_MARKINGS
NUMBER_OF_ONE_MARKINGS      = 90
NUMBER_OF_SUB_ONE_MARKINGS  = 4 * 90 + NUMBER_OF_ONE_MARKINGS #think: 9 between each whole degree, but draw 4 with lines and use the 5 spaces between lines as implicit markings

NUMBER_OF_MARKINGS = 90 + 4*90 # 90 whole numbers, 4 markings between each of the whole markings (draw only each line with 0.2 deg separation)
ANGLE_SEPARATION_DEGFREE = 0.2
NUMBER_OF_SUB_ONE_MARKINGS_PER_MARKING = 1/ANGLE_SEPARATION_DEGFREE # = 5

TEXT_DISTANCE_FROM_MARKINGS = 5




## SVM gamma PROTRACTOR LINES ##

if draw_markings:
    for n_marking in range(NUMBER_OF_MARKINGS+1):
                theta = degrees_to_radians(THETA_START_DEGREE + n_marking*ANGLE_SEPARATION_DEGFREE)

                # function choosing r_length and angle_text
                r_length = 0
                plot_text = False
                if   (n_marking % (10*NUMBER_OF_SUB_ONE_MARKINGS_PER_MARKING)) == 0:
                            r_length = L_TEN_MARKINGS
                            plot_text = True
                            angle_text = int( (n_marking / (10*NUMBER_OF_SUB_ONE_MARKINGS_PER_MARKING))*10 )

                elif (n_marking %  (5*NUMBER_OF_SUB_ONE_MARKINGS_PER_MARKING)) == 0:
                            r_length = L_FIVE_MARKINGS
                            plot_text = True
                            angle_text = int( (n_marking / (5*NUMBER_OF_SUB_ONE_MARKINGS_PER_MARKING))*5 )

                elif (n_marking %  (1*NUMBER_OF_SUB_ONE_MARKINGS_PER_MARKING)) == 0:
                            r_length = L_ONE_MARKINGS

                else:                                  
                    r_length = L_SUB_ONE_MARKINGS
                

                #r_displacement = R_DIFFERENCE_BETWEEN_KUGGHJUL_RADIUS_AND_MARKINGS_RADIUS_AT_THETA_270_DEGREES*np.cos(theta)
                r_displacement = 0
                draw_radial_line(R_MARKINGS_MAX, r_length, theta, r_outward_displacement = r_displacement, color_string="g")
                if plot_text:
                    draw_degree_text(theta, R_MARKINGS_MAX-r_length-TEXT_DISTANCE_FROM_MARKINGS+r_displacement, angle_text)




Delta_theta_axis_radius_circle_left = abs(np.arctan(Y_DISPLACEMENT_ROTATION_AXIS_HOLE_CENTER/R_KUGGHJUL_INNER_RADIUS))
Delta_theta_axis_radius_circle_down = abs(np.arctan(X_DISPLACEMENT_ROTATION_AXIS_HOLE_CENTER/R_KUGGHJUL_INNER_RADIUS))


# DRAW CIRCLE ARC FOR THE KUGGHJUL_INNER_RADIUS #
draw_circle(r=3, x_0=0, y_0=0) #plumb hole
draw_circle(r=18, x_0=X_DISPLACEMENT_ROTATION_AXIS_HOLE_CENTER,
                  y_0=Y_DISPLACEMENT_ROTATION_AXIS_HOLE_CENTER)
draw_arc_of_circle( r=R_KUGGHJUL_INNER_RADIUS,
                    x_0=X_DISPLACEMENT_ROTATION_AXIS_HOLE_CENTER,
                    y_0=Y_DISPLACEMENT_ROTATION_AXIS_HOLE_CENTER,
                    theta_start = np.pi - Delta_theta_axis_radius_circle_left,
                    theta_end = 3*np.pi/2 + Delta_theta_axis_radius_circle_down)

#TODO: shift the radial lines with (r,theta) --> (x,y), then shift in x,y based on some math i will do, then (x,y) --> (r, theta), plot those

#   TODO: DET SER NÄSTAN RÄTT UT MEN DET ÄR DET INTE! (SE SKILLNAD I AVSTÅND MELLAN GRÅ OCH RÖD LINJE FÖR THETA =270 DEG OCH +45 DEG OCH 3*PI/2 RAD)
#   TODO: HITTA NÅGON TRANSFORM MELLAN DEN GRÅA CIRKELN OCH DEN RÖDA (OLIKA RADIE OCH OLIKA CIRKELCENTRUM)
#         FÖRSKJUT FRÅN GRÅA TILL RÖDA CIRKEL, SEN FÖRSKJUT ALLA RADIER MED EN KONSTANT OFFSET (AVSTÅND MELLAN KUGGHJULRADIE OCH BÖRJAN AV GRADMARKERINGARNA)

## SET NICE PLOT PROPERTIES ##

ax=plt.gca()
ax.set_rticks([R_MARKINGS_MAX, 0])
ax.set_xticks([]) # theta ticks
ax.set_thetalim(degrees_to_radians(THETA_START_DEGREE), degrees_to_radians(THETA_END_DEGREE))
ax.set_rlim(R_LIM_MIN, R_LIM_MAX)
if export_figure:
    matplotlib.pyplot.savefig("SVM_g_protractor_lines.pdf", format='pdf', bbox_inches='tight')
elif export_figure_as_test:
    matplotlib.pyplot.savefig("SVM_g_protractor_lines_TEST.pdf", format='pdf', bbox_inches='tight')      
plt.show()