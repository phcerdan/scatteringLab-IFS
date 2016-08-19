# -*- coding: utf-8 -*-
"""
Created on Fri Jun 24 14:05:20 2016
Code to plot the ouput from static light scattering experiments. This code
should be run once the sample, standard or both have been completed. 
For observing running experiments the code hotPlotLive.py should be run.
For issues email bmansel@gmail.com or track down P H Cedan

SlumLabs inc. 2016
"""

import os
import natsort
import numpy
import matplotlib.pyplot as plt
import argparse

def AverageDataFolder(base_path,plot_figure=0,flag_write=True):
    """
    Read data files from each subdirectory of the base_path. Write and plot data
    depending on imput flags. Return the base_path intensity average 
    (average of all sub directory average) and the angles.
    
    plot_figure, input for the number of the plot, should be incremented for
    each time the function is called. If set to 0 no plots will be produced.
    """    
    subdirectories = [d for d in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, d))]
    subdirectories = natsort.natsorted(subdirectories)
    #loop through directory and create and avergage file for each subdirectory
    average_filename = 'averaged_out.txt'
    #I_mat =[]    
    i = 0
    for subdir in subdirectories:
        subdir_path = os.path.join(base_path,subdir)
        if os.path.exists( os.path.join(subdir_path,average_filename) ):
            print(subdir_path+average_filename+' already exists')        
            #import existing data for average at the end           
            data_out = numpy.genfromtxt(os.path.join(subdir_path,average_filename))
            averaged_data = numpy.array(data_out[:,1])
            angles = data_out[:,0]
            #os.remove( os.path.join(subdir_path,average_filename))
        else:
            files = os.listdir(subdir_path)     
            #files = [d for d in os.listdir(subdir_path) if os.path.isdir(os.path.join(subdir_path, d))]
            onlyfiles_path = [os.path.join(subdir_path,f) for f in files if os.path.isfile(os.path.join(subdir_path,f))]
            onlyfiles_path = natsort.natsorted(onlyfiles_path)          
            averaged_data = []
            angles = []
            for f in onlyfiles_path:
                data = numpy.genfromtxt(f,delimiter = ',')       
                #data = pandas.read_csv(f)
                averaged_data.append(numpy.mean(data))
                angle = os.path.basename(f).split('_')[0]
                angles.append(float(angle))
                
            data_out = numpy.array([angles,averaged_data])
            #numpy.savetxt(os.path.join(subdir_path,average_filename),(angles,averaged_data)) 
            if flag_write == True:            
                numpy.savetxt(os.path.join(subdir_path,average_filename),numpy.transpose(data_out)) 
        if i == 0:
            I_mat = numpy.array(averaged_data)
            #print(I_mat)
            #print(I_mat.size)
        else:    
            I_mat = numpy.vstack([I_mat,averaged_data])
        i = i + 1
        
    # calculate mean and save data in the base_path 
    if I_mat.ndim > 1:
        I_mat_mean = numpy.mean(I_mat,axis=0)
    else:
        I_mat_mean = I_mat
    average_data_out = numpy.array([angles,I_mat_mean])
    if flag_write == True:
        numpy.savetxt(os.path.join(base_path,'measurement_average.txt'),numpy.transpose(average_data_out))
    if plot_figure != 0:
        plt.figure(plot_figure)
        #plt.ion()
        #rc('font', **{'family': 'serif', 'serif': ['Computer Modern']})
        #rc('text', usetex=True)
        if I_mat.ndim > 1:
            for c in range(len(I_mat[:,0])):
                plt.plot(angles,I_mat[c,:],'.',alpha=0.3,label = str(c+1))
        #plt.rc('text', usetex=True)
        plt.plot(angles, I_mat_mean, label = 'average')
        plt.yscale('log')
        plt.xscale('log')
        plt.legend(loc='upper right')
        plt.title(base_path)
        plt.grid(True)
        plt.xlabel(r'$\theta$ $[deg.]}$')
        #plt.xlabel(r'$\mathrm{xlabel\;with\;\LaTeX\;font}$')
        plt.ylabel(r'I($\theta$) $[a.u.]$')
        plt.show()
    return I_mat_mean, angles

# Run if executed, but not if it is imported from other python script
if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Calculate average intensity and output .txt file of the intensity and angle the plot',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--input_path','-i', required=True, action='store',
            help='The path that the experimental data was written to')
    parser.add_argument('--standard_path', action='store',
            default='',
            help='The path that the standard measurement data was written to e.g. 50nm particles or toluene')   
    parser.add_argument('--save_data_path', action='store',
            default='',
            help='The path that the normalized measurement data was written to e.g. C:/users/path/to/output.txt')
    parser.add_argument('--no_write_output', action='store',
            default=False,
            help='Avoid saving the output.')  
    args = parser.parse_args()
    #============================================================ 
    base_path_smp = os.path.abspath(args.input_path)
    write_flag = not args.no_write_output
    I_mat_mean_smp, angles = AverageDataFolder(base_path_smp,1,write_flag)
    if args.standard_path != '':
        base_path_std = os.path.abspath(args.standard_path)
        normalized_save_path = ''
        if args.save_data_path == '':
            normalized_save_path = os.path.join(base_path_smp,'normalized_measurement_average.txt')
        else:
            normalized_save_path = os.path.abspath(args.save_data_path)
        I_mat_mean_std, angles = AverageDataFolder(base_path_std,2,write_flag)   
        normalized_I = numpy.divide(I_mat_mean_smp,I_mat_mean_std)
        normalized_data_out = numpy.array([angles,normalized_I])
        numpy.savetxt(normalized_save_path,numpy.transpose(normalized_data_out))
        plt.figure(3)
        plt.plot(angles, normalized_I,'-o')
        plt.yscale('log')
        plt.xscale('log')
        plt.title('Normalized Intensity vs Angle')
        plt.grid(True)
        plt.xlabel(r'$\theta$ $[deg.]}$')
        #plt.xlabel(r'$\mathrm{xlabel\;with\;\LaTeX\;font}$')
        plt.ylabel(r'I($\theta$) $[a.u.]$')
        plt.show()      