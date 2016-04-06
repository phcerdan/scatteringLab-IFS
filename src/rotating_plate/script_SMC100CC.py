#============================================================ 
#Initialization Start 
#The script within Initialization Start and Initialization End is needed for properly  
#initializing IOPortClientLib and Comm and Interface for SMC100 instrument. 
#The user should copy this code as is and specify correct paths here. 
import sys 
#Command Interface DLL can be found here. 
print "Adding location of Newport.SMC 100.CommandInterface.dll to sys.path" 
#sys.path.append(r'C:\Program Files (x86)\Newport\MotionControl\SMC100\Bin') 
sys.path.append(r'C:\Users\bmansel\dev\MotionControl\SMC100\Bin') 

#Brad mod
#===============
import os
import time
import subprocess
#===============

# The CLR module provide functions for interacting with the underlying  
# .NET runtime 
import clr 
# Add reference to assembly and import names from namespace 
clr.AddReferenceToFile("Newport.SMC100.CommandInterface.dll") 
#clr.AddReference("Newport.SMC100.CommandInterface") 
from CommandInterfaceSMC100 import * 
import System 
#============================================================ 
# Instrument Initialization 
instrumentKey="COM5" 
print 'Instrument Key=>', instrumentKey
# create a device instance 
SMC = SMC100() 
#GetDeviceList(SMC)
result = SMC.OpenInstrument(instrumentKey) 
print 'Instrument opened?=>', result
# Get positive software limit 
result, response, errString = SMC.SR_Get(1)  
if result == 0 : 
   print 'positive software limit=>', response 
else: 
 print 'Error=>',errString 
# Get negative software limit 
result, response, errString = SMC.SL_Get(1)  
if result == 0 : 
   print 'negative software limit=>', response 
else: 
 print 'Error=>',errString 
# Get controller revision information 
result, response, errString = SMC.VE(1)  
if result == 0 : 
   print 'controller revision=>', response 
else: 
 print 'Error=>',errString 
# Get current position 
result, response, errString = SMC.TP(1)  
if result == 0 : 
   print 'position=>', response 
else: 
 print 'Error=>',errString 
#TEST CODE:::
# GET STATE TS.
print SMC.TS(1)
#Get Acceleration setting and velocity
SMC.AC_Set(1,5)
print "acceleration:"
print SMC.AC_Get(1)
empt, vel, empt2 = SMC.VA_Get(1)
SMC.VA_Set(1,10)
print "velocity:"
print SMC.VA_Get(1)

# Rotate to 10

#a, b = SMC.PA_Set(1,20) 
#print a, b
# Rotate relative 2 and loop through
#print SMC.PT_Get(1,5.0) #print time to rotate

startAng = 50
endAng = 150
stepSize = 1

# Call python (cpython) script:
exe_path=os.path.abspath("C:/Users/bmansel/dev/scatteringLab-IFS/src/correlator/correlator.py")
option_time = '10'
option_mode = 'single'
option_out_folder = os.path.abspath("C:/Users/bmansel/dev/tmp")

#Move to start position and wait:
SMC.PA_Set(1,float(180-startAng))
time.sleep(15)
for angle in range(180-startAng, 180-endAng, -1):
	SMC.PA_Set(1,float(angle))
	time.sleep(2)
	subprocess.call(['python',exe_path,
	'--duration', option_time,'--mode', option_mode,
	'--out_folder', option_out_folder, '--angle', str(angle)])
	print angle
	#print add, rotTime, errString
	#time.sleep(rotTime)

# Get current position 
result, response, errString = SMC.TP(1)  
if result == 0 : 
   print 'position=>', response 
else: 
 print 'Error=>',errString 
# Unregister device 
SMC.CloseInstrument()
#SMC.UnregisterComponent(); 
