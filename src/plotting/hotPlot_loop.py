# -*- coding: utf-8 -*-
"""
Loop through an experimental folder and run hotplot with the same standard.
This way we don't have to make hotplot overly long

@author: brad
"""

import os
import numpy as np
import subprocess

experiment_dir = '/home/brad/Documents/Data/Amy_measurements/'
hotPlot_dir = '/home/brad/repository_local/scatteringLab-IFS/src/plotting/hotPlot.py'
standard_path = '/home/brad/Documents/Data/Amy_measurements/52nm_2ul_per_ml_nD0p5'

experiment_data = os.listdir(experiment_dir) 

test =1

for experiment in experiment_data:
    subprocess.call(['python',os.path.abspath(hotPlot_dir),'--input_path',os.path.join(experiment_dir,experiment),'--standard_path',os.path.abspath(standard_path)])    
    print os.path.join(experiment_dir,experiment)
    print test
    test = test + 1