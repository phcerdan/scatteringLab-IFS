#!/usr/bin/python
import sys, os, string
import subprocess #Call binary
import argparse #Read command line args
import shutil # Copy

#GLOBALS:
#output_file_from_correlator = 'corr.dat'
# correlator_executable:
#exe_path =>  = "C:/Users/bmansel/dev/correlator/build/Debug/sample.exe"

def call_correlator(c_exe_path, duration, mode):
    "Calls c executable correlator with arguments: duration mode"
    if(not os.path.exists(c_exe_path)):
        sys.exit("Executable not found: " + os.path.abspath(c_exe_path))

    # if c_exe_path is not succesfull raise error from python.
    subprocess.check_call([c_exe_path, str(duration), str(mode)]);

def ensure_dir(filename):
    "Ensure dir exists"
    d = os.path.dirname(filename)
    if not os.path.exists(d):
        os.makedirs(d)

def copy_output(c_exe_path, new_filename):
    "Copy output from c executable to a new_filename"
    d = os.path.dirname(c_exe_path)
    # This name depends on hard-coded c script.
    default_out = os.path.join(d,'corr.dat')
    ensure_dir(new_filename)
    shutil.copy2(default_out, new_filename)

# Run if executed, but not if it is imported from other python script
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Wrapper for c++ binary managing correlator.')
    parser.add_argument('--out_folder', action='store',
            help='output folder to store results')
    parser.add_argument('--angle', action='store', type=float,
        help='angle from goniometer')
    parser.add_argument('--duration', action='store', type=int,
            help='duration for the correlator in seconds (C++)' )
    parser.add_argument('--mode', action='store',
            choices=['single', 'quad', 'dual'],
            help='Mode for the correlator')
    args = parser.parse_args()
    #TODO transform arguments to variables

    exe_path=os.path.abspath("C:/Users/bmansel/dev/scatteringLab-IFS/build/correlator/Debug/sample.exe")
    mode = args.mode
    duration = args.duration
    angle = args.angle
    out_folder = os.path.abspath(args.out_folder)
    call_correlator(exe_path, duration, mode);

    # Build the output string from input parameters:
    angle_string = "{:2f}".format(angle)
    outfile = "_".join([angle_string, str(duration), str(mode)])
    outfile = ".".join([outfile, 'out'])
    newfile = os.path.join(out_folder, outfile)

    copy_output(exe_path, newfile)

    sys.exit(1) # Just in case get called by other python subprocess

