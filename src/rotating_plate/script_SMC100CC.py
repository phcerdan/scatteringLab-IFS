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
clr.AddReferenceToFile('Newport.SMC100.CommandInterface.dll') 
#clr.AddReference("Newport.SMC100.CommandInterface.dll") 
from CommandInterfaceSMC100 import * 
import System 
#============================================================ 
# create a device instance 
SMC = SMC100() 
CAddr = 1 # This is default, and you don't want to change it.
print 'Devices: ' , SMC.GetDevices()
# Instrument Initialization 
instrumentKey="COM6" 
print 'Instrument Key=>', instrumentKey
result = SMC.OpenInstrument(instrumentKey) 
SMC.MM_Set(CAddr, 1) # Set from Disable to Ready state. (0 is the oposite)
if result == 0 : 
   print 'Instrument opened'
else: 
 print 'ERROR correlator instrument not opened', result
 exit()
# Get positive software limit 
result, response, errString = SMC.SR_Get(CAddr)  
if result == 0 : 
   print 'positive software limit=>', response 
else: 
 print 'Error=>',errString 
# Get negative software limit 
result, response, errString = SMC.SL_Get(CAddr)  
if result == 0 : 
   print 'negative software limit=>', response 
else: 
 print 'Error=>',errString 
# Get controller revision information 
result, response, errString = SMC.VE(CAddr)  
if result == 0 : 
   print 'controller revision=>', response 
else: 
 print 'Error=>',errString 
# Get current position 
result, response, errString = SMC.TP(CAddr)  
if result == 0 : 
   print 'Initial position=>', response 
else: 
 print 'Error=>',errString 
# GET STATE TS.
stateResult, dummy1, stateString, dummy2 = SMC.TS(CAddr)
print 'State TS (0 success, 34: good READY from DISABLE) : ', SMC.TS(CAddr)
if stateString != '34' :
   print 'State: ' , stateString, ' different that 34, exit. Try to run it again'
   SMC.CloseInstrument()
   exit()
#Get Acceleration setting and velocity
SMC.AC_Set(1,5)
print "acceleration:", SMC.AC_Get(CAddr)
SMC.VA_Set(1,10)
print "velocity:" , SMC.VA_Get(CAddr)
# Rotate to 10
#a, b = SMC.PA_Set(1,20) 
#print a, b
# Rotate relative 2 and loop through
#print SMC.PT_Get(1,5.0) #print time to rotate


#USER INPUT
# Add instrumentKey as a user variable to choose (use get devices to see devices available)
### ROTATING PLATE
startScatAng = 50
endScatAng = 140
stepSize = 1
if startScatAng < 0 or endScatAng < 0: 
   print 'BAD INPUT: Input angles are in term of scattering angle, not in terms of the rotating plate RotPlateAngle = ScatAngle - 90. Negative scattering angles are not allowed: startScatAngle: ', startScatAng, 'endScatAngle', endScatAng
   SMC.CloseInstrument()
   exit()
else:
   print 'startScatAng: ', startScatAng , ' ; endScatAng: ' , endScatAng, '; stepSize: ' , stepSize
### END ROTATING PLATE
### CORRELATOR
correlator_script = "C:/Users/bmansel/dev/scatteringLab-IFS/src/correlator/correlator.py"
correlator_out_folder = "C:/Users/bmansel/dev/tmp/test1/tol/"
correlator_time = '5'
correlator_mode = 'single'
#do not modify path variables
correlator_exe_path = os.path.abspath(correlator_script)
correlator_out_folder_path = os.path.abspath(correlator_out_folder)
## END CORRELATOR CONFIG
#Move to start position and wait:
# Convert to rotating plate angles:
startRotPlateAng = startScatAng - 90
endRotPlateAng = endScatAng - 90

SMC.PA_Set(1,float(startRotPlateAng))
time.sleep(15)
for rotAngle in range(startRotPlateAng, endRotPlateAng + 1, stepSize):
	scatAngle = rotAngle + 90
	SMC.PA_Set(1,float(rotAngle))
	time.sleep(2)
        # Call python (cpython) script:
	subprocess.call(['python',correlator_exe_path,
	'--duration', correlator_time,'--mode', correlator_mode,
	'--out_folder', correlator_out_folder_path, '--angle', str(scatAngle)])
	print 'Scattering angle:' , scatAngle,  ' ; (RP= ', rotAngle , ')'
	# Get current position 
	result, response, errString = SMC.TP(CAddr)  
	if result == 0 : 
		print 'current rotating plate position=>', response 
	else: 
		print 'Error=>',errString 
	#print add, rotTime, errString
	#time.sleep(rotTime)

# Get current position 
result, response, errString = SMC.TP(CAddr)  
if result == 0 : 
   print 'position=>', response 
else: 
 print 'Error=>',errString 
# Unregister device 
#SMC.UnregisterComponent(); 
SMC.CloseInstrument()
