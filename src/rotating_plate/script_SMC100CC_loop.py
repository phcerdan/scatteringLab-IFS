#============================================================ 
#Initialization Start 
#The script within Initialization Start and Initialization End is needed for properly  
#initializing IOPortClientLib and Comm and Interface for SMC100 instrument. 
#The user should copy this code as is and specify correct paths here. 
import sys 
#Command Interface DLL can be found here. 
print "Adding location of Newport.SMC 100.CommandInterface.dll to sys.path" 
sys.path.append(r'C:\Program Files (x86)\Newport\MotionControl\SMC100\Bin') 
#sys.path.append(r'C:\Users\bmansel\dev\MotionControl\SMC100\Bin') 

#Brad mod
#===============
import os
import time
import subprocess
import argparse #Read command line args
#===============

# The CLR module provide functions for interacting with the underlying  
# .NET runtime 
import clr 
# Add reference to assembly and import names from namespace 
clr.AddReferenceToFile('Newport.SMC100.CommandInterface.dll') 
#clr.AddReference("Newport.SMC100.CommandInterface.dll") 
from CommandInterfaceSMC100 import * 
import System 

# Run if executed, but not if it is imported from other python script
if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='SMC100 homebuilt controller for the rotating plate connected to the correlator',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    #ROTATING PLATE OPTIONS
    parser.add_argument('--st_ang', action='store', type=int,
            default=30,
            help='start scatering angle')
    parser.add_argument('--end_ang', action='store', type=int,
            default=130,
            help='end scatering angle')
    parser.add_argument('--step_size_rotating', action='store', type=int,
            default=1,
            help='step size for the rotating plate')
    parser.add_argument('--instrument_key', action='store',
            default='COM6',
            help='Rotating Plate instrument key: COMx')
    parser.add_argument('--num_its', action='store', type=int,
            default=1,
			help='enter an integer to run the experiment over many times')
    #CORRELATOR OPTIONS
    parser.add_argument('--correlator_script', action='store',
            default="C:/Users/bmansel/dev/scatteringLab-IFS/src/correlator/correlator.py",
            help='script "correlator.py" which control the correlator')
    parser.add_argument('--out_folder', action='store',
            default="C:/Users/bmansel/dev/tmp/test1/tol/",
            help='output folder to store results')
    parser.add_argument('--correlator_duration', action='store',
    	    default='10',
            help='duration for the correlator in seconds (C++), type:string' )
    parser.add_argument('--correlator_mode', action='store',
            choices=['single', 'quad', 'dual'],
	    default='single',
            help='Mode for the correlator')
    args = parser.parse_args()
    #============================================================ 

    # create a device instance 
    SMC = SMC100() 

    ##### CHECK ROTATING PLATE IS LISTENING#########

    CAddr = 1 # This is default, and you don't want to change it.
    print 'Devices: ' , SMC.GetDevices()
    # Instrument Initialization 
    instrumentKey= args.instrument_key
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

    ##### END OF CHECKS #########

    ### ROTATING PLATE

    startScatAng = args.st_ang
    endScatAng = args.end_ang
    stepSize = args.step_size_rotating
    if startScatAng < 0 or endScatAng < 0: 
       print 'BAD INPUT: Input angles are in term of scattering angle, not in terms of the rotating plate RotPlateAngle = ScatAngle - 90. Negative scattering angles are not allowed: startScatAngle: ', startScatAng, 'endScatAngle', endScatAng
       SMC.CloseInstrument()
       exit()
    else:
       print 'startScatAng: ', startScatAng , ' ; endScatAng: ' , endScatAng, '; stepSize: ' , stepSize
    ### END ROTATING PLATE
    ### CORRELATOR
    #do not modify path variables
    correlator_exe_path = os.path.abspath(args.correlator_script)
    correlator_out_folder_path = os.path.abspath(args.out_folder)
    ## END CORRELATOR CONFIG

    # Convert to rotating plate angles:
    startRotPlateAng = startScatAng - 90
    endRotPlateAng = endScatAng - 90
	#Loop through angles to run an experiment many times
    for iteration in range(1, args.num_its+1, 1):
        correlator_out_folder_path_loop = correlator_out_folder_path + '/'+ str(iteration)
        #Move to start position and wait:
    	SMC.PA_Set(1,float(startRotPlateAng))
    	time.sleep(15)
        for rotAngle in range(startRotPlateAng, endRotPlateAng + 1, stepSize):
			scatAngle = rotAngle + 90 
			SMC.PA_Set(1,float(rotAngle)-0.7)
			time.sleep(2)
			# Call python (cpython) script:
			subprocess.call(['python',correlator_exe_path,
			'--duration', args.correlator_duration,'--mode', args.correlator_mode,
			'--out_folder', correlator_out_folder_path_loop, '--angle', str(scatAngle)])
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
    print "Adding location of Newport.SMC 100.CommandInterface.dll to sys.path" 
    sys.path.append(r'C:\Users/bmansel/dev/scatteringLab-IFS/src/plotting')	
    subprocess.call(['python',os.path.abspath('C:/Users/bmansel/dev/scatteringLab-IFS/src/plotting/hotPlot.py'),'--input_path',correlator_out_folder_path])