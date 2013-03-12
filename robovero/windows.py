import sys


def fullPortName(portname):
  """ 
  Args: 
  
  - Given a port-name (of the form COM7, COM12, CNCA0, etc.) 
  
  Return:
  
  - a full name suitable for opening with the Serial class.
  
  """
  if (sys.platform == "win32"):
    import itertools, re
    m = re.match('^COM(\d+)$', portname)
    if m and int(m.group(1)) < 10:
        return portname
    return '\\\\.\\' + portname

def enumerateSerialPorts():
  """ Uses the Win32 registry to return a iterator of serial 
      (COM) ports existing on this computer.
  """
  if (sys.platform == "win32"):
    import _winreg as winreg
    path = 'HARDWARE\\DEVICEMAP\\SERIALCOMM'
    try:
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, path)
    except WindowsError:
        raise IterationError

    for i in itertools.count():
        try:
          val = winreg.EnumValue(key, i)
          if ("\\Device\\USBSER" in str(val[0])):
            yield (str(val[0]), str(val[1]))
        except EnvironmentError:
          break
