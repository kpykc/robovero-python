from internals import robocaller

def aeroLoopOn():
  """Flash the onboard LED.
  """
  return robocaller("aeroLoopOn", "void")
  
def aeroLoopOff():
  """Let user control the onboard LED.
  """
  return robocaller("aeroLoopOff", "void")

def aeroInit(accelerometer, gyro):
  """LALALALALA
  """
  return robocaller("aeroInit", "void", accelerometer, gyro)

def setThrottle(throttle):
  """ :O
  """
  return robocaller("setThrottle", "void", throttle)

def getMotorCommands():
  """ D:
  """
  
  motor_commands = robocaller("getMotorCommands", "int")
  for i in range(len(motor_commands)):
    motor_commands[i] = (motor_commands[i] + 2**15) % 2**16 - 2**15
  return motor_commands

def stopAllMotors():
  """ asdfadsf
  
  """
  return robocaller("stopAllMotors", "void")
