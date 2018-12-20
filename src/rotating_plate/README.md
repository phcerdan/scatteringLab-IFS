# Newport Configuration

Install driver for SMC100 controller, and for the RS232 Adapter
SMC100CC webpage: https://www.newp rtcom/p/SMC100CC

The CommandInterface.dll is documented in the official Newport documentation,
however (at 18 Dec 2018) it cannot be found in their webpage.
We just re-used the version that we already had from other computer.

```
sys.path.append(r'C:\Program Files (x86)\Newport\MotionControl\SMC100\Bin') 
clr.AddReferenceToFile('Newport.SMC100.CommandInterface.dll') 
```


YOU NEED IRON PYTHON TO WORK WITH .NET libraries. (PythonNet is not enough)

download and install iron python (2.7.5)
To use any -X:Frames command you need root privileges (run as admin from GUI)
Install pip in iron python (as root):
"C:\Program Files (x86)\IronPython 2.7\ipy64.exe" -X:Frames -m ensurepip
Install pyvisa (communication with RS232 cable standard)
"C:\Program Files (x86)\IronPython 2.7\ipy64.exe" -X:Frames -m pip pyvisa
