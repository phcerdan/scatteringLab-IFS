# -*- coding: utf-8 -*-
"""
Code to take the experiment averaged files that have been created by hotplot 
and chenging the angle to scattering vector. Also it can apply a correction for
some reflection that has been roughly estimated from small angle neutron 
scattering data. The code can run through all of the experimental .txt files
in an experimental directory.

@author: brad
"""

import os
import numpy as np
import matplotlib.pyplot as plt

experiment_dir = '/home/brad/Documents/Data/Amy_measurements'
experiment_data = os.listdir(experiment_dir) 