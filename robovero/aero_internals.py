from internals import robocaller

def aeroLoopOn():
  """Flash the onboard LED.
  """
  return robocaller("aeroLoopOn", "void")
  
def aeroLoopOff():
  """Let user control the onboard LED.
  """
  return robocaller("aeroLoopOff", "void")

def aeroInit():
  """LALALALALA
  """
  return robocaller("aeroInit", "void")

def setThrottle(throttle):
  """ :O
  """
  return robocaller("setThrottle", "void", throttle)
  
def setLevelRollPID(P,I,D):
  """ :O
  """
  return robocaller("setLevelRollPID", "void", P*1000,I*1000,D*1000)

def setLevelPitchPID(P,I,D):
  """ :O
  """
  return robocaller("setLevelPitchPID", "void", P*1000,I*1000,D*1000)
  
def setLevelGyroRollPID(P,I,D):
  """ :O
  """
  return robocaller("setLevelGyroRollPID", "void", P*1000,I*1000,D*1000)

def setLevelGyroPitchPID(P,I,D):
  """ :O
  """
  return robocaller("setLevelGyroPitchPID", "void", P*1000,I*1000,D*1000)

def getMotorCommands():
  """ D:
  """
  
  motor_commands = robocaller("getMotorCommands", "int")
  for i in range(len(motor_commands)):
    motor_commands[i] = (motor_commands[i] + 2**15) % 2**16 - 2**15
  return motor_commands

def getFlightAngles():
  """ D:
  """
  
  flight_angles = robocaller("getFlightAngles", "int")
  for i in range(len(flight_angles)):
    flight_angles[i] = (flight_angles[i] + 2**15) % 2**16 - 2**15
  return flight_angles
  
def getGyroReadings():
  """ D:
  """
  
  gyro_readings = robocaller("getGyroReadings", "int")
  for i in range(len(gyro_readings)):
    gyro_readings[i] = (gyro_readings[i] + 2**15) % 2**16 - 2**15
  return gyro_readings
  
def getAccelReadings():
  """ D:
  """
  
  accel_readings = robocaller("getAccelReadings", "int")
  for i in range(len(accel_readings)):
    accel_readings[i] = ((accel_readings[i] + 2**15) % 2**16 - 2**15)
  return accel_readings
  
def getFlightCmds():
  """ D:
  """
  
  flight_cmds = robocaller("getFlightCmds", "int")
  for i in range(len(flight_cmds)):
    flight_cmds[i] = ((flight_cmds[i] + 2**15) % 2**16 - 2**15)
  return flight_cmds

def stopAllMotors():
  """ asdfadsf
  
  """
  return robocaller("stopAllMotors", "void")
