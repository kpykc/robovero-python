""" wrapper functions to set parameters for aerodroid
"""
from internals import robocaller

def aeroLoopOn():
  """ Start the main loop
  """
  return robocaller("aeroLoopOn", "void")
  
def aeroLoopOff():
  """ Stop the main loop
  """
  return robocaller("aeroLoopOff", "void")

def aeroInit():
  """ Initialize variables, IMU, and PID values to default values
  """
  return robocaller("aeroInit", "void")

def setThrottle(throttle):
  """ Set the throttle.
  """
  return robocaller("setThrottle", "void", throttle)
  
def setLevelRollPID(P,I,D):
  """ Set Roll PID values used in calculateFlightError. Used on angles
  
  PID values are scaled properly internally
  """
  return robocaller("setLevelRollPID", "void", P*1000,I*1000,D*1000)

def setLevelPitchPID(P,I,D):
  """ Set pitch PID values used in calculateFlightError. Used on angles
  
  PID values are scaled properly internally
  """
  return robocaller("setLevelPitchPID", "void", P*1000,I*1000,D*1000)
  
def setLevelGyroRollPID(P,I,D):
  """ Set roll PID values used in calculateFlightError. Used on gyro readings
  
  PID values are scaled properly internally
  """
  return robocaller("setLevelGyroRollPID", "void", P*1000,I*1000,D*1000)

def setLevelGyroPitchPID(P,I,D):
  """ Set pitch PID values used in calculateFlightError. Used on gyro readings
  
  PID values are scaled properly internally
  """
  return robocaller("setLevelGyroPitchPID", "void", P*1000,I*1000,D*1000)
  
def setAltitudePID(P,I,D):
  """ Set Altitude control PID values
  
  PID values are scaled properly internally
  """
  return robocaller("setAltitudePID", "void", P*1000,I*1000,D*1000)

def getMotorCommands():
  """ Read motor commands from the RoboVero
  
  return: list
  """
  
  motor_commands = robocaller("getMotorCommands", "int")
  for i in range(len(motor_commands)):
    motor_commands[i] = (motor_commands[i] + 2**15) % 2**16 - 2**15
  return motor_commands

def getFlightAngles():
  """ Read angles found using the algorithm used to fly
  
  return: list
  """
  
  flight_angles = robocaller("getFlightAngles", "int")
  for i in range(len(flight_angles)):
    flight_angles[i] = (flight_angles[i] + 2**15) % 2**16 - 2**15
  return flight_angles
  
def getBalanceAngles():
  """ Read angles found using balance filter
  
  
  return: list
  """
  
  balance_angles = robocaller("getBalanceAngles", "int")
  for i in range(len(balance_angles)):
    balance_angles[i] = (balance_angles[i] + 2**15) % 2**16 - 2**15
  return balance_angles
  
def getGyroReadings():
  """ Get raw gyro readings

  return: list
  """
  
  gyro_readings = robocaller("getGyroReadings", "int")
  for i in range(len(gyro_readings)):
    gyro_readings[i] = (gyro_readings[i] + 2**15) % 2**16 - 2**15
  return gyro_readings
  
def getAccelReadings():
  """ Get raw accelerometer readings
  
  return: list
  """
  
  accel_readings = robocaller("getAccelReadings", "int")
  for i in range(len(accel_readings)):
    accel_readings[i] = ((accel_readings[i] + 2**15) % 2**16 - 2**15)
  return accel_readings
  
def getFlightCmds():
  """ Get intermediate values from calculateFlightErrors.
  
  return: list
  """
  
  flight_cmds = robocaller("getFlightCmds", "int")
  for i in range(len(flight_cmds)):
    flight_cmds[i] = ((flight_cmds[i] + 2**15) % 2**16 - 2**15)
  return flight_cmds
  
def getAltitudeReadings():
  """ Get current height from ground
  """
  return robocaller("getAltitudeReadings", "int")

def stopAllMotors():
  """ Sends a speed = 0 command to all motors. aeroLoopOff is a better
  way to kill
  
  """
  return robocaller("stopAllMotors", "void")
  
def maintainConnection():
  """ tells RoboVero that host is still here. If after 5 iterations of
  aeroLoop and no connection is maintained, RoboVero will automatically 
  stop
  
  """
  return robocaller("maintainConnection", "void")
  
def setAngleLimit(angle_limit):
  """ Set the maximum angle before RoboVero shuts down the motors
  
  angle_limit: angle limit in degrees
  
  """
  return robocaller("setAngleLimit", "void", angle_limit)
  
def setTargetAltitude(altitude):
  """ Set target altitude to try to maintain
  
  """
  return robocaller("setTargetAltitude", "void", altitude)

def toggleAltitudeControl(toggle):
  """ Turns altitude control off if toggle = 0. Otherwise turns it on
  
  """
  return robocaller("toggleAltitudeControl", "void", toggle)
  
def changeMew(new_mew):
  """ changes the mew used in weighted average in balance filter.
  
  Found in aeroangle.c
  
  """
  return robocaller("changeMew", "void", new_mew*1000)

def setLowPassU(new_low_pass_u):
  """ Sets the low_pass_u found in aerodroid.c. Should be used for low 
  pass filter on accelerometer readings. (currently not used)
  """
  return robocaller("setLowPassU", "void", new_low_pass_u * 1000)
