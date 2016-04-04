# Newport Configuration

Install driver for SMC100 controller, and for the RS232 Adapter

Install (if not already installed ) Anaconda python.

If anaconda python is the default, go to command prompt and type:
pip install pyvisa

[try the python script provided by Newport](http://assets.newport.com/webDocuments-EN/images/NewportPython.zip)

pyvisa is just a wrapper around VISA library. Go download the library from national instruments.
Choose the latest windows version. (you need an account (free-fake it) to download)
[nivisa](https://www.ni.com/visa/)

[Test pyvisa:](http://pyvisa.readthedocs.org/en/stable/getting.html)
test pyvisa with:
python
import visa
rm = visa.ResourceManager()
print (rm.list_resources())



YOU NEED IRON PYTHON TO WORK WITH .NET libraries. (PythonNet is not enough)

download and install iron python (2.7.5)
To use any -X:Frames command you need root privileges (run as admin from GUI)
Install pip in iron python (as root):
"C:\Program Files (x86)\IronPython 2.7\ipy64.exe" -X:Frames -m ensurepip
Install pyvisa (communication with RS232 cable standard)
"C:\Program Files (x86)\IronPython 2.7\ipy64.exe" -X:Frames -m pip pyvisa
