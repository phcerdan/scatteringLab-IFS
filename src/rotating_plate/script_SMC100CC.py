#============================================================ 
#Initialization Start 
#The script within Initialization Start and Initialization End is needed for properly  
#initializing IOPortClientLib and Comm and Interface for SMC100 instrument. 
#The user should copy this code as is and specify correct paths here. 
import sys 
#Command Interface DLL can be found here. 
print "Adding location of Newport.SMC 100.CommandInterface.dll to sys.path" 
sys.path.append(r'C:\Program Files (x86)\Newport\MotionControl\SMC100\Bin') 

# The CLR module provide functions for interacting with the underlying  
# .NET runtime (PHC: Ignore this and pip install pyvisa for direct access.
import clr 
# Add reference to assembly and import names from namespace 
clr.AddReferenceToFile("Newport.SMC100.CommandInterface.dll") 
from CommandInterfaceSMC100 import * 
import System 
#============================================================ 
# Instrument Initialization 
instrument="COM5" 
print 'Instrument Key=>', instrument 
# create a device instance 
SMC = SMC100() 
result = SMC100.OpenInstrument(instrumentKey) 
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
# Unregister device 
SMC.UnregisterComponent(); 
