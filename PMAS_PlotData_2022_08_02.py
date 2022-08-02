##====================================================##
##     Project: PLOT DATA (specifically for PMAS)
##        File: PMAS_PlotData[2022-08-02].py
##      Author: GOTTFRID OLSSON 
##     Created: 2022-06-17, 10:56
##     Updated: 2022-08-02, 13:3
##       About: Plot data from CSV with matplotlib.
##              Plot-settings in JSON, export as PDF.
##====================================================##


#---------------#
#    IMPORTS    #
#---------------#

import matplotlib.pyplot as plt         # to plot

#------------------#
#  MANUAL IMPORTS  # in order to avoid a lot of plot-files together with the PMAS-files
#------------------#

# JSON
import json                         # to save/write to JSON


## FUNCTIONS ##

def JSON_read(readFilePath):
    with open(readFilePath, 'r') as jsonfile:
        JSON = json.load(jsonfile)
    print("DONE: Reading JSON: " + readFilePath)
    return JSON

def JSON_write(writeFilePath, JSON_data):
  with open(writeFilePath, 'w', encoding='utf-8') as jsonfile:
    #jsonfile.write(JSON) #commented out //2022-02-20
    json.dump(JSON_data, jsonfile, ensure_ascii=False) #changed from "dumps()" to "dump()" and added encoding 'utf-8' and ensure_ascii=False //2022-02-20
  print("DONE: Writing JSON: " + writeFilePath)

import easygui


#JSON_readFilePath = "JSON/"+ "CONFIG" + ".json" #keeping this line for myself when I'm working with figures //2022-07-05
JSON_readFilePath = easygui.fileopenbox(title="Please choose your JSON-file")
J = JSON_read(JSON_readFilePath)



#--------------------#
# GET DATA FROM JSON #
#--------------------#

filepath_csv            = J['filepath']['csv']
filepath_pdf            = J['filepath']['pdf']

figure_height           = J['figure_size']['height_cm'] # [cm]
figure_width            = J['figure_size']['width_cm']  # [cm]

font_size_axis          = J['font_size']['axis']   # [pt]
font_size_tick          = J['font_size']['tick']   # [pt]
font_size_legend        = J['font_size']['legend'] # [pt]

LaTeX_and_CMU           = J['LaTeX_and_CMU']

subplot_setup_rows      = J['subplot_setup']['rows']
subplot_setup_columns   = J['subplot_setup']['columns']
subplot_setup_subplots  = J['subplot_setup']['total_subplots'] #TODO?: raise error if "total != rows*columns"


## DECLARE VARIABLE NAMES ##

subplots = range(subplot_setup_subplots)

subplot_num            = [i for i in subplots]
plot_type              = []

dataset_label          = []
dataset_CSV_column_x   = []
dataset_CSV_column_y   = []

line_color             = []
line_style             = []
line_width             = []

marker_type            = []
marker_size            = []
marker_thickness       = []
marker_facecolor       = []

errorbar_on            = []
errorbar_constant_on   = []
errorbar_constant_x_pm = []
errorbar_constant_y_pm = []
errorbar_CSV_column_x  = []
errorbar_CSV_column_y  = []
errorbar_size          = []
errorbar_linewidth     = []
errorbar_capthickness  = []

axis_x_label           = []
axis_x_limit_min       = []
axis_x_limit_max       = []
axis_x_scale           = []
axis_x_invert          = []
axis_x_float_precision = []

axis_y_label           = []
axis_y_limit_min       = []
axis_y_limit_max       = []
axis_y_scale           = []
axis_y_invert          = []
axis_y_float_precision = []

legend_on              = []
legend_alpha           = []
legend_location        = []

grid_major_on          = []
grid_major_linewidth   = []
grid_minor_on          = []
grid_minor_linewidth   = []


# functions
import matplotlib.pyplot
import matplotlib


def cm_2_inch(cm):
    return cm/2.54


def set_LaTeX_and_CMU(LaTeX_and_CMU_on):
    if LaTeX_and_CMU_on:
        matplotlib.rcParams.update({
    "text.usetex": True,
    "font.family": "serif", 
    "font.serif" : ["Computer Modern Roman"]
    })
    print("DONE: set_LaTeX_and_CMU: " + str(LaTeX_and_CMU_on))


def set_font_size(axis, tick, legend):
    matplotlib.rc('font',   size=axis)      #2022-06-21: not sure what the difference is, to test later on!
    matplotlib.rc('axes',   titlesize=axis) #2022-06-21: not sure what the difference is, to test later on!
    matplotlib.rc('axes',   labelsize=axis) #2022-06-21: not sure what the difference is, to test later on!
    matplotlib.rc('xtick',  labelsize=tick)
    matplotlib.rc('ytick',  labelsize=tick)
    matplotlib.rc('legend', fontsize=legend)
    print("DONE: set_font_size: (axis, tick, legend): " + str(axis) + ", " + str(tick) + ", " + str(legend))


def set_axis_labels(ax, xLabel, yLabel, axNum):
    ax.set_xlabel(str(xLabel))
    ax.set_ylabel(str(yLabel))
    print("DONE: set_axis_labels: on axs: " + str(axNum))


def set_legend(ax, legend_on, alpha, location, axNum):
      if legend_on:
            ax.legend(framealpha=alpha, loc=location)
      print("DONE: set_legend: (on, alpha, location): " + str(legend_on) + ", " + str(alpha) + ", " + str(location) + " on axs: " + str(axNum))


def set_grid(ax, grid_major_on, grid_major_linewidth, grid_minor_on, grid_minor_linewidth, axNum):
      if grid_major_on:
        ax.grid(grid_major_on, which='major', linewidth=grid_major_linewidth) 
      if grid_minor_on:
        ax.minorticks_on()
        ax.grid(grid_minor_on, which='minor', linewidth=grid_minor_linewidth)
      print("DONE: set_grid: grid_major: " + str(grid_major_on) +", grid_minor: "+ str(grid_minor_on)+  " on axs: " + str(axNum))


def set_axis_scale(ax, xScale_string, yScale_string, axNum):
    ax.set_xscale(xScale_string)
    ax.set_yscale(yScale_string)
    print("DONE: set_axis_scale: X: " + str(xScale_string) + ", Y: " + str(yScale_string) + " on axs: " + str(axNum))


def set_axis_limits(ax, xmin, xmax, ymin, ymax, axNum):
    if not xmin: xmin = None
    if not xmax: xmax = None
    if not ymin: ymin = None
    if not ymax: ymax = None
    
    ax.set_xlim(xmin, xmax)
    ax.set_ylim(ymin, ymax)
    print("DONE: set_axis_limits: x=(" + str(xmin) + ", " + str(xmax)+ ") and y=(" + str(ymin) + ", " + str(ymax)+ ") on axs: " + str(axNum))


def set_axis_invert(ax, x_invert, y_invert, axNum):
    if x_invert: ax.invert_xaxis()
    if y_invert: ax.invert_yaxis()
    print("DONE: set_axis_invert: x: " + str(x_invert) + ", y: " + str(y_invert) + " on axs: " + str(axNum))


def set_commaDecimal_with_precision_x_axis(ax, xAxis_precision, axNum):
    xFormatString = '{:.' + str(xAxis_precision) + 'f}'
    ax.get_xaxis().set_major_formatter( matplotlib.ticker.FuncFormatter(lambda x, pos: xFormatString.format(x).replace('.', ',')) )    
    print("DONE: set_commaDecimal_with_precision_x_axis: "+str(xAxis_precision) + " on axs: "+str(axNum))


def set_commaDecimal_with_precision_y_axis(ax, yAxis_precision, axNum):
    yFormatString = '{:.' + str(yAxis_precision) + 'f}'
    ax.get_yaxis().set_major_formatter( matplotlib.ticker.FuncFormatter(lambda x, pos: yFormatString.format(x).replace('.', ',')) )    
    print("DONE: set_commaDecimal_with_precision_y_axis: "+str(yAxis_precision) + " on axs: "+str(axNum))


def set_layout_tight(fig):
    fig.tight_layout()
    print("DONE: set_layout_tight")


def align_labels(fig):
    fig.align_labels()
    print("DONE: align_labels")
    

def export_figure_as_pdf(filePath):
    matplotlib.pyplot.savefig(filePath, format='pdf', bbox_inches='tight')#, metadata={"Author" : "Gottfrid Olsson", "Title" : "", "Keywords" : "Created with PlotData by Gottfrid Olsson"}) ##this could be implemented in the future, 2022-06-21
    print("DONE: export_figure_as_pdf: " + filePath)


# errorbar
def plot_errorbar(ax, data_x, data_y, errorbar_on, errorbar_x, errorbar_y, errorbar_size, errorbar_linewidth, errorbar_capthickness, data_label, line_color, line_style, line_width, marker_type, marker_size, marker_thickness, marker_facecolor, ax_num):
    if errorbar_on:  
        out = ax.errorbar(data_x, data_y, label=data_label, color=line_color, linestyle=line_style, linewidth=line_width, \
            marker=marker_type, markersize=marker_size, markeredgewidth=marker_thickness, markerfacecolor=marker_facecolor, \
                xerr=errorbar_x, yerr=errorbar_y, elinewidth=errorbar_linewidth, capsize=errorbar_size, capthick=errorbar_capthickness)
        print("DONE: Plotted data with 'errorbar' on axs: " + str(ax_num))
    else:
        out = ax.plot(data_x, data_y, label=data_label, color=line_color, linestyle=line_style, linewidth=line_width, \
        marker=marker_type, markersize=marker_size, markeredgewidth=marker_thickness, markerfacecolor=marker_facecolor)
        print("DONE: Plotted data with 'errorbar' (without errorbars) on axs: " + str(ax_num))
    
    return out

#---------------#
# ASSIGN VALUES #
#---------------#

###### TODO: do this for standard JSON-values ##//2022-07-05: is it worth it? why just not copy and paste and change the values you need to change? I can create a JSON-template to copy forall plot_types
###### TODO: figure out how to "check" if a value in JSON exists (if not, don't overwrite standard values; if exists, do write over)
 

## PER SUBPLOT ##

for i in subplots:
    plot_type.append(               J['subplot_settings'][i]['datasets']['plot_type']                       )
    dataset_label.append(           J['subplot_settings'][i]['datasets']['dataset_label']                   )  

    dataset_CSV_column_x.append(    J['subplot_settings'][i]['datasets']['CSV_column_x']                    )
    dataset_CSV_column_y.append(    J['subplot_settings'][i]['datasets']['CSV_column_y']                    )

    axis_x_label.append(            J['subplot_settings'][i]['datasets']['axis']['x']['label']              )
    axis_x_limit_min.append(        J['subplot_settings'][i]['datasets']['axis']['x']['limit']['min']       )
    axis_x_limit_max.append(        J['subplot_settings'][i]['datasets']['axis']['x']['limit']['max']       )
    axis_x_scale.append(            J['subplot_settings'][i]['datasets']['axis']['x']['scale']              )
    axis_x_invert.append(           J['subplot_settings'][i]['datasets']['axis']['x']['invert']             )
    axis_x_float_precision.append(  J['subplot_settings'][i]['datasets']['axis']['x']['float_precision']    )   

    axis_y_label.append(            J['subplot_settings'][i]['datasets']['axis']['y']['label']              )
    axis_y_limit_min.append(        J['subplot_settings'][i]['datasets']['axis']['y']['limit']['min']       )
    axis_y_limit_max.append(        J['subplot_settings'][i]['datasets']['axis']['y']['limit']['max']       )
    axis_y_scale.append(            J['subplot_settings'][i]['datasets']['axis']['y']['scale']              )
    axis_y_invert.append(           J['subplot_settings'][i]['datasets']['axis']['y']['invert']             )
    axis_y_float_precision.append(  J['subplot_settings'][i]['datasets']['axis']['y']['float_precision']    )

    legend_on.append(               J['subplot_settings'][i]['datasets']['legend']['on']                    )
    legend_alpha.append(            J['subplot_settings'][i]['datasets']['legend']['alpha']                 )
    legend_location.append(         J['subplot_settings'][i]['datasets']['legend']['location']              )   

    grid_major_on.append(           J['subplot_settings'][i]['datasets']['grid']['major']['on']             )
    grid_major_linewidth.append(    J['subplot_settings'][i]['datasets']['grid']['major']['linewidth']      )
    grid_minor_on.append(           J['subplot_settings'][i]['datasets']['grid']['minor']['on']             )    
    grid_minor_linewidth.append(    J['subplot_settings'][i]['datasets']['grid']['minor']['linewidth']      )



    bin_line_color = []
    bin_line_style = []
    bin_line_width = []

    bin_marker_type      = []
    bin_marker_size      = []
    bin_marker_thickness = []
    bin_marker_facecolor = []

    bin_errorbar_on            = []
    bin_errorbar_CSV_column_x  = []
    bin_errorbar_CSV_column_y  = []
    bin_errorbar_size          = []
    bin_errorbar_linewidth     = []
    bin_errorbar_capthickness  = []
    bin_errorbar_constant_on   = []
    bin_errorbar_constant_x_pm = []
    bin_errorbar_constant_y_pm = []

    for k in range(len(plot_type[i])):
        # TODO: "if":s that select what 'plot_type_settings' to get from JSON (line, marker, errorbar, ...)
        bin_line_color.append(              J['subplot_settings'][i]['datasets']['plot_type_settings']['line']['color'][k]                  )
        bin_line_style.append(              J['subplot_settings'][i]['datasets']['plot_type_settings']['line']['style'][k]                  )
        bin_line_width.append(              J['subplot_settings'][i]['datasets']['plot_type_settings']['line']['width'][k]                  )

        bin_marker_type.append(             J['subplot_settings'][i]['datasets']['plot_type_settings']['marker']['type'][k]                 )
        bin_marker_size.append(             J['subplot_settings'][i]['datasets']['plot_type_settings']['marker']['size'][k]                 )
        bin_marker_thickness.append(        J['subplot_settings'][i]['datasets']['plot_type_settings']['marker']['thickness'][k]            )
        bin_marker_facecolor.append(        J['subplot_settings'][i]['datasets']['plot_type_settings']['marker']['facecolor'][k]            )
        
        bin_errorbar_on.append(             J['subplot_settings'][i]['datasets']['plot_type_settings']['errorbar']['on'][k]                 )
        bin_errorbar_CSV_column_x.append(   J['subplot_settings'][i]['datasets']['plot_type_settings']['errorbar']['CSV_column_x'][k]       )
        bin_errorbar_CSV_column_y.append(   J['subplot_settings'][i]['datasets']['plot_type_settings']['errorbar']['CSV_column_x'][k]       )
        bin_errorbar_size.append(           J['subplot_settings'][i]['datasets']['plot_type_settings']['errorbar']['size'][k]               )
        bin_errorbar_linewidth.append(      J['subplot_settings'][i]['datasets']['plot_type_settings']['errorbar']['linewidth'][k]          )
        bin_errorbar_capthickness.append(   J['subplot_settings'][i]['datasets']['plot_type_settings']['errorbar']['capthickness'][k]       )
        bin_errorbar_constant_on.append(    J['subplot_settings'][i]['datasets']['plot_type_settings']['errorbar']['constant']['on'][k]     )
        bin_errorbar_constant_x_pm.append(  J['subplot_settings'][i]['datasets']['plot_type_settings']['errorbar']['constant']['x_pm'][k]   )
        bin_errorbar_constant_y_pm.append(  J['subplot_settings'][i]['datasets']['plot_type_settings']['errorbar']['constant']['y_pm'][k]   )


    line_color.append(bin_line_color)
    line_style.append(bin_line_style)
    line_width.append(bin_line_width)

    marker_type.append(     bin_marker_type     )
    marker_size.append(     bin_marker_size     )
    marker_thickness.append(bin_marker_thickness)
    marker_facecolor.append(bin_marker_facecolor)
    
    errorbar_on.append(             bin_errorbar_on             )
    errorbar_CSV_column_x.append(   bin_errorbar_CSV_column_x   )
    errorbar_CSV_column_y.append(   bin_errorbar_CSV_column_y   )
    errorbar_size.append(           bin_errorbar_size           )
    errorbar_linewidth.append(      bin_errorbar_linewidth      )
    errorbar_capthickness.append(   bin_errorbar_capthickness   )
    errorbar_constant_on.append(    bin_errorbar_constant_on    )
    errorbar_constant_x_pm.append(  bin_errorbar_constant_x_pm  )
    errorbar_constant_y_pm.append(  bin_errorbar_constant_y_pm  )


print("DONE: get_JSON_data.py")

# CSV

import pandas as pd


## CONSTANTS ##

CSV_DELIMITER = ','


## FUNCTIONS ##

def CSV_read(readFilePath):
    #print("In progress: Reading CSV" + CSV_filePath)
    CSV =  pd.read_csv(readFilePath, sep=CSV_DELIMITER)
    print("DONE: Reading CSV: " + readFilePath)
    return CSV

# i'm not sure how to do this nicely. yet. //2022-02-04, 19:12
def CSV_write(CSV_data, writeFilePath):
    #print("In progress: Exporting CSV")
    #headers = get_header(CSV_data)
    #CSV_data.to_csv(writeFilePath)
    #with open(writeFilePath, 'w', newline='') as csvfile:
    #    CSV = csv.writer(csvfile, delimiter = CSV_DELIMITER)
    #    CSV.writerows(CSV_data)
    #print("Done: Writing CSV: " + writeFilePath)
    raise Exception("This function is not yet coded. Sorry. //2022-02-04")

def CSV_get_header(CSV_data):
    return CSV_data.columns.values

#------------#
#    MAIN    #
#------------#


def main():
    print("=== PLOT DATA Start ===")

    CSV_data   = CSV_read( filepath_csv)
    CSV_header = CSV_get_header(CSV_data)

    set_LaTeX_and_CMU( LaTeX_and_CMU) # needs to run before "fig, axs = [...]" to parse LaTeX correctly
    set_font_size( font_size_axis,  font_size_tick,  font_size_legend)

    fig, axs = plt.subplots( subplot_setup_rows,  subplot_setup_columns, figsize=( cm_2_inch( figure_width),  cm_2_inch( figure_height)))
      #TODO: different sized subplots? ; https://www.statology.org/subplot-size-matplotlib/

    for i in range( subplot_setup_subplots): # forall subplots

        if  subplot_setup_subplots == 1:
            axs_i = axs     # necessary to avoid several for-loops (since object "AxesSubplot" is not subscriptable)
        else:
            axs_i = axs[i]
            
        for k in range(len( plot_type[i])):  # forall types of plots in each subplot


            if  plot_type[i][k] == "errorbar":
                print("Plotting 'errorbar' on x: " + str(CSV_header[ dataset_CSV_column_x[i][k]]) +", and y: "+ str(CSV_header[ dataset_CSV_column_y[i][k]]) + " on axs: " + str(i))
                
                data_x     = CSV_data[CSV_header[ dataset_CSV_column_x[i][k]]]
                data_y     = CSV_data[CSV_header[ dataset_CSV_column_y[i][k]]]
                errorbar_x = CSV_data[CSV_header[ errorbar_CSV_column_x[i][k]]]
                errorbar_y = CSV_data[CSV_header[ errorbar_CSV_column_y[i][k]]]

                if  errorbar_on[i][k] and  errorbar_constant_on[i][k]:
                    errorbar_x = [ errorbar_constant_x_pm[i][k] for x_pm in data_x]
                    errorbar_y = [ errorbar_constant_y_pm[i][k] for y_pm in data_y]

                plot_errorbar(
                    axs_i, data_x, data_y,  errorbar_on[i][k], errorbar_x, errorbar_y, \
                     errorbar_size[i][k],  errorbar_linewidth[i][k],  errorbar_capthickness[i][k], \
                     dataset_label[i][k],  line_color[i][k],  line_style[i][k],  line_width[i][k], \
                     marker_type[i][k],  marker_size[i][k],  marker_thickness[i][k],  marker_facecolor[i][k], i
                    )

            ## HERE GOES OTHER 'plot_types' ##
            #if  plot_type[i] == "blahblah"
                # ...

            else:
                print("ERROR: keyword 'plot_type' = " + str( plot_type[i][k]) + " is not implemented (yet). Sorry for the inconvenience.")




        set_axis_scale(   axs_i,  axis_x_scale[i],  axis_y_scale[i], i)
        set_axis_labels(  axs_i,  axis_x_label[i],  axis_y_label[i], i)
        set_axis_invert(  axs_i,  axis_x_invert[i],  axis_y_invert[i], i)
        set_axis_limits(  axs_i,  axis_x_limit_min[i],  axis_x_limit_max[i],  axis_y_limit_min[i], axis_y_limit_max[i], i)
  

        set_grid(         axs_i,  grid_major_on[i],  grid_major_linewidth[i],  grid_minor_on[i],  grid_minor_linewidth[i], i) # set_grid must be after set_axis_scale for some reason (at least with 'log')
        set_legend(       axs_i,  legend_on[i],  legend_alpha[i],  legend_location[i], i)
        
        if  axis_x_scale[i] != 'log':
             set_commaDecimal_with_precision_x_axis(axs_i,  axis_x_float_precision[i], i)
        if  axis_y_scale[i] != 'log':
             set_commaDecimal_with_precision_y_axis(axs_i,  axis_y_float_precision[i], i)
        

    align_labels(fig)
    set_layout_tight(fig)
    export_figure_as_pdf( filepath_pdf)

    print("=== PLOT DATA End ===")      
    plt.show()



if __name__ == "__main__":
    main()








