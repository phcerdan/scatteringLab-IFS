# -*- coding: utf-8 -*-
"""
Code to take the experiment averaged files that have been created by hotplot 
and chang the angle to scattering vector and apply a correction for
some reflection that has been roughly estimated from small angle neutron 
scattering data. The code can run through all of the experimental .txt files
in an experimental directory.

A port of some crappy MATLAB code

@author: brad
"""

import os
import numpy as np
import matplotlib.pyplot as plt

experiment_dir = '/home/brad/Documents/Data/Amy_measurements/' #User input

experiment_list = os.listdir(experiment_dir) 
corr = 0.05 # The value of the reflection to be subtracted_off

std_data = np.genfromtxt(os.path.abspath('/home/brad/Documents/Data/Amy_measurements/52nm_2ul_per_ml_nD0p5/measurement_average.txt')) #User input
q = 4*np.pi*1.33/5320*np.sin(np.multiply(np.pi/180,np.divide(std_data[:,0],2)))
mietheory_52nm = np.genfromtxt(os.path.abspath('/home/brad/Documents/Data/52nm_mietheory.txt'))

for experiment in experiment_list:
    if experiment != '52nm_2ul_per_ml_nD0p5':    
        data_no_corr = np.genfromtxt(os.path.join(experiment_dir,experiment,'normalized_measurement_average.txt'))
        data_raw = np.genfromtxt(os.path.join(experiment_dir,experiment,'measurement_average.txt'))  
        save_loc = os.path.join(experiment_dir,experiment,'corrected_data.txt')       
        fig_save_loc = os.path.join(experiment_dir,experiment,'corrected_data.png')        
        I_part_flip_smp = np.flipud(data_raw[34:,1])
        I_raw_smp_corr = np.subtract(data_raw[34:,1],np.multiply(corr,I_part_flip_smp))
        I_part_flip_std = np.flipud(std_data[34:,1])
        I_raw_std_corr = np.subtract(std_data[34:,1],np.multiply(corr,I_part_flip_std))
        I_part1_corr = np.divide(data_raw[:34,1],std_data[:34,1])        
        I_part2_corr = np.divide(I_raw_smp_corr,I_raw_std_corr)
        I_corr = np.hstack((I_part1_corr,I_part2_corr))
        normalized_data_out = np.array([q,I_corr])
        np.savetxt(save_loc,np.transpose(normalized_data_out))        
        plt.plot(q, I_corr,'-o', label = 'corrected data')
        plt.plot(q,np.divide(data_raw[:,1],std_data[:,1]), label = 'raw data')        
        plt.yscale('log')
        plt.xscale('log')
        plt.grid(True)
        plt.xlabel('q [A^-1]')
        #plt.xlabel(r'$\mathrm{xlabel\;with\;\LaTeX\;font}$')
        plt.ylabel('I(q) [a.u.]')
        plt.legend()
        plt.savefig(fig_save_loc)
        plt.show()
        plt.clf()