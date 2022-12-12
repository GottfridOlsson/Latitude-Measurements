##====================================================##
##     Project: SVM gamma
##        File: protractor_markings.py
##      Author: GOTTFRID OLSSON 
##     Created: 2022-12-02
##     Updated: 2022-12-12
##       About: Plot data in a polar plot.
##====================================================##

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import math




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

def get_radial_distance_from_point_to_cricle_at_origin_at_angle(circle_radius, x_coordination_point, y_coordination_point, angle_radians):
    r_0 = circle_radius
    a, b = x_coordination_point, y_coordination_point
    alpha = angle_radians
    
    k = get_directional_coefficient_for_line_from_angle(alpha)

    # SOLVE SYSTEM OF EQUATION FOR CIRCLE AND LINE THROUGH POINT # (done on paper)
    x_plus, x_minus = get_x_roots_line_intersecting_circle_problem(r_0, a, b, k)
    y_plus, y_minus = get_y_roots_line_intersecting_circle_problem(r_0, a, b, k)

    x_intersect, y_intersect = None, None

    # PICK RIGHT ROOTS BASED ON ANGLE # (verified in Desmos)
    if math.isclose(alpha, 0, rel_tol=1e-6) or math.isclose(alpha, 2*np.pi, rel_tol=1e-6):
        x_intersect = x_plus
        y_intersect = b
    
    if 0 < alpha < np.pi/2:
        x_intersect = x_plus
        y_intersect = y_plus

    if math.isclose(alpha, np.pi/2, rel_tol=1e-6):
        x_intersect = a
        y_intersect = y_plus 

    if np.pi/2 < alpha < np.pi:
        x_intersect = x_minus
        y_intersect = y_plus
    
    if math.isclose(alpha, np.pi, rel_tol=1e-6):
        x_intersect = x_minus
        y_intersect = b

    if np.pi < alpha < 3*np.pi/2:
        x_intersect = x_minus
        y_intersect = y_minus
    
    if math.isclose(alpha, 3*np.pi/2, rel_tol=1e-6):
        x_intersect = a
        y_intersect = y_minus

    if 3*np.pi/2 < alpha < 2*np.pi:
        x_intersect = x_plus
        y_intersect = y_minus

    radial_distance = get_distance_between_two_points(a, b, x_intersect, y_intersect)

    return radial_distance

def get_directional_coefficient_for_line_from_angle(angle_radians):
    alpha = angle_radians

    if abs(alpha) > 2*np.pi:
        print(f"ERROR: angle |{alpha}| > 2*pi. Make the angle lie within the range [0, 2*pi] to use this function")
        pass

    if 0 <= alpha < np.pi or math.isclose(alpha, 2*np.pi, rel_tol=1e-6):
        return np.tan(alpha)

    if np.pi <= alpha < 3*np.pi/2:
        return np.tan(alpha-np.pi)

    if math.isclose(alpha, 3*np.pi/2, rel_tol=1e-6):
        return 10**20 # "infty"
    
    if 3*np.pi/2 < alpha < 2*np.pi:
        return np.tan(alpha - np.pi)
    
    print(f"Angle {alpha} radians were not caught by the cases implemented in get_directional_coefficient_for_line_from_angle")

def get_x_roots_line_intersecting_circle_problem(circle_radius, x_coordination_point, y_coordination_point, directional_coefficient_line):
    r_0 = circle_radius
    a = x_coordination_point
    b = y_coordination_point
    k = directional_coefficient_line

    #define terms in solution to quadratic equation
    alpha = k**2 + 1
    beta = r_0**2 - (b-k*a)**2
    gamma = k*(b-k*a)

    x_plus  = -gamma/alpha + np.sqrt( beta/alpha + gamma**2/alpha**2 )
    x_minus = -gamma/alpha - np.sqrt( beta/alpha + gamma**2/alpha**2 )

    return x_plus, x_minus
    
def get_y_roots_line_intersecting_circle_problem(circle_radius, x_coordination_point, y_coordination_point, directional_coefficient_line):
    r_0 = circle_radius
    a = x_coordination_point
    b = y_coordination_point
    k = directional_coefficient_line


    #define terms in solution to quadratic equation
    if k != 0:
        c = 1/k
    else:
        c = 10**20 #"infty"

    alpha = c**2 + 1
    beta = r_0**2 - (a-b*c)**2
    gamma = c*(a-b*c)

    y_plus  = -gamma/alpha + np.sqrt( beta/alpha + gamma**2/alpha**2 )
    y_minus = -gamma/alpha - np.sqrt( beta/alpha + gamma**2/alpha**2 )

    return y_plus, y_minus

def get_distance_between_two_points(a, b, c, d):
    return np.sqrt( (a-c)**2 + (b-d)**2 )

matplotlib.rcParams.update({
    "text.usetex": True,
    "font.family": "serif", 
    "font.serif" : ["Computer Modern Roman"]
    })
plt.figure(figsize=(10,10)) #15,15
plt.axes(projection = 'polar')







## DEFINE VARIABLES ##
draw_markings = True
export_figure = True
export_figure_as_test = False


R_LIM_MAX = 510
R_LIM_MIN = 0

R_KUGGHJUL_INNER_RADIUS = 474                 # mm, //2022-12-08
X_DISPLACEMENT_ROTATION_AXIS_HOLE_CENTER = 29 # mm, relative the plump hole center //2022-12-08
Y_DISPLACEMENT_ROTATION_AXIS_HOLE_CENTER = -21 # mm, relative the plump hole center //2022-12-08

R_AXISHOLE_CIRCLE_RADIUS_AT_THETA_270_DEGREES = X_DISPLACEMENT_ROTATION_AXIS_HOLE_CENTER + R_KUGGHJUL_INNER_RADIUS

R_DISTANCE_BETWEEN_KUGGHJUL_RADIUS_AND_MARKINGS= 25 # mm,
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
ANGLE_SEPARATION_DEGREE = 0.2
NUMBER_OF_SUB_ONE_MARKINGS_PER_MARKING = 1/ANGLE_SEPARATION_DEGREE # = 5

TEXT_DISTANCE_FROM_MARKINGS = 5




## SVM gamma PROTRACTOR LINES ##

# PREPARATION #

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


radial_distance_from_origin_to_circle_for_gear = []
angles_radians_third_quadrant_step_one_degree = degrees_to_radians( np.linspace(180, 270, 270-180+1) )

for i in range(len(angles_radians_third_quadrant_step_one_degree)):
            radial_distance_from_origin_to_circle_for_gear.append(

                #why negative X and Y displacement below?
                # since the calculation in "get_radial_distance_from_point_to_cricle_at_origin_at_angle" is for a circle at (0,0) and a point at (a,b)
                # a coordinate shift is needed to make the origin at (-a,-b) such that the point is at (0,0)
                get_radial_distance_from_point_to_cricle_at_origin_at_angle(
                    R_KUGGHJUL_INNER_RADIUS,
                    -X_DISPLACEMENT_ROTATION_AXIS_HOLE_CENTER,
                    -Y_DISPLACEMENT_ROTATION_AXIS_HOLE_CENTER,
                    angles_radians_third_quadrant_step_one_degree[i]))
            #test:
            #draw_radial_line(radial_distance_from_origin_to_circle_for_gear[i], radial_distance_from_origin_to_circle_for_gear[i], angles_radians_third_quadrant_step_one_degree[i])



# DRAW PROTRACTOR LINES ##

if draw_markings:
    for n_marking in range(NUMBER_OF_MARKINGS+1):
                theta = degrees_to_radians(THETA_START_DEGREE + n_marking*ANGLE_SEPARATION_DEGREE)
                r_distance_origin_to_kugghjul_circle = get_radial_distance_from_point_to_cricle_at_origin_at_angle(
                    R_KUGGHJUL_INNER_RADIUS,
                    -X_DISPLACEMENT_ROTATION_AXIS_HOLE_CENTER,
                    -Y_DISPLACEMENT_ROTATION_AXIS_HOLE_CENTER,
                    theta
                    #why negative X and Y displacement above?
                    # since the calculation in "get_radial_distance_from_point_to_cricle_at_origin_at_angle" is for a circle at (0,0) and a point at (a,b)
                    # a coordinate shift is needed to make the origin at (-a,-b) such that the point is at (0,0)    
                )

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
                

                draw_radial_line(r_distance_origin_to_kugghjul_circle-R_DISTANCE_BETWEEN_KUGGHJUL_RADIUS_AND_MARKINGS, r_length, theta, color_string="g")
                if plot_text:
                    draw_degree_text(theta, r_distance_origin_to_kugghjul_circle-R_DISTANCE_BETWEEN_KUGGHJUL_RADIUS_AND_MARKINGS-r_length-TEXT_DISTANCE_FROM_MARKINGS, angle_text)




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