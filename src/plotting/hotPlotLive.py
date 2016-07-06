# -*- coding: utf-8 -*-
"""
Created on Tue Jun 28 13:53:48 2016
Live plot data from a subdirectory
@author: SlumLabs
"""
import matplotlib as plt
import matplotlib.animation as animation
import time
import os
import natsort
import numpy



def animate_plotting(subdir_path,):
    average_filename = 'averaged_out.txt'  
    if os.path.exists( os.path.join(subdir_path,average_filename) ):
            print(subdir_path+average_filename+' already exists please use hotPlot.py')        
            #import existing data for average at the end           
#            data_out = numpy.genfromtxt(os.path.join(subdir_path,average_filename))
#            averaged_data = numpy.array(data_out[:,1])
#            angles = data_out[:,0]
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
        fig = plt.plot(angles, averaged_data,'o')
        plt.yscale('log')
        plt.xscale('log')
        plt.legend(loc='upper right')
        plt.title(base_path)
        plt.grid(True)
        plt.xlabel(r'$\theta$ $[deg.]}$')
        #plt.xlabel(r'$\mathrm{xlabel\;with\;\LaTeX\;font}$')
        plt.ylabel(r'I($\theta$) $[a.u.]$')
        

base_path = 'C:\cygdrive\c\Users\bmansel\dev\test2'
subdir = '1'
subdir_path = os.path.join(base_path,subdir)
ani = animation.FuncAnimation(fig, animate_plotting, interval=1000)
plt.show()                
#            data_out = numpy.array([angles,averaged_data])
    