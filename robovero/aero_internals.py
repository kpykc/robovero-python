""" wrapper functions to set parameters for aerodroid
"""
from internals import RoboCaller

def aeroLoopOn():
  """ Start the main loop
  """
  return RoboCaller().call("aeroLoopOn", "void")

def aeroLoopOff():
  """ Stop the main loop
  """
  return RoboCaller().call("aeroLoopOff", "void")

def aeroInit():
  """ Initialize variables, IMU, and PID values to default values
  """
  return RoboCaller().call("aeroInit", "void")

def setThrottle(throttle):
  """ Set the throttle.
  """
  return RoboCaller().call("setThrottle", "void", throttle)

def setLevelRollPID(P,I,D):
  """ Set Roll PID values used in calculateFlightError. Used on angles

  PID values are scaled properly internally
  """
  return RoboCaller().call("setLevelRollPID", "void", P*1000,I*1000,D*1000)

def setLevelPitchPID(P,I,D):
  """ Set pitch PID values used in calculateFlightError. Used on angles

  PID values are scaled properly internally
  """
  return RoboCaller().call("setLevelPitchPID", "void", P*1000,I*1000,D*1000)

def setLevelGyroRollPID(P,I,D):
  """ Set roll PID values used in calculateFlightError. Used on gyro readings

  PID values are scaled properly internally
  """
  return RoboCaller().call("setLevelGyroRollPID", "void", P*1000,I*1000,D*1000)

def setLevelGyroPitchPID(P,I,D):
  """ Set pitch PID values used in calculateFlightError. Used on gyro readings

  PID values are scaled properly internally
  """
  return RoboCaller().call("setLevelGyroPitchPID", "void", P*1000,I*1000,D*1000)

def setAltitudePID(P,I,D):
  """ Set Altitude control PID values

  PID values are scaled properly internally
  """
  return RoboCaller().call("setAltitudePID", "void", P*1000,I*1000,D*1000)

def getMotorCommands():
  """ Read motor commands from the RoboVero

  return: list
  """

  motor_commands = RoboCaller().call("getMotorCommands", "int")
  for i in range(len(motor_commands)):
    motor_commands[i] = (motor_commands[i] + 2**15) % 2**16 - 2**15
  return motor_commands

def getFlightAngles():
  """ Read angles found using the algorithm used to fly

  return: list
  """

  flight_angles = RoboCaller().call("getFlightAngles", "int")
  for i in range(len(flight_angles)):
    flight_angles[i] = (flight_angles[i] + 2**15) % 2**16 - 2**15
  return flight_angles

def getBalanceAngles():
  """ Read angles found using balance filter


  return: list
  """

  balance_angles = RoboCaller().call("getBalanceAngles", "int")
  for i in range(len(balance_angles)):
    balance_angles[i] = (balance_angles[i] + 2**15) % 2**16 - 2**15
  return balance_angles

def getGyroReadings():
  """ Get raw gyro readings

  return: list
  """

  gyro_readings = RoboCaller().call("getGyroReadings", "int")
  for i in range(len(gyro_readings)):
    gyro_readings[i] = (gyro_readings[i] + 2**15) % 2**16 - 2**15
  return gyro_readings

def getAccelReadings():
  """ Get raw accelerometer readings

  return: list
  """

  accel_readings = RoboCaller().call("getAccelReadings", "int")
  for i in range(len(accel_readings)):
    accel_readings[i] = ((accel_readings[i] + 2**15) % 2**16 - 2**15)
  return accel_readings

def getFlightCmds():
  """ Get intermediate values from calculateFlightErrors.

  return: list
  """

  flight_cmds = RoboCaller().call("getFlightCmds", "int")
  for i in range(len(flight_cmds)):
    flight_cmds[i] = ((flight_cmds[i] + 2**15) % 2**16 - 2**15)
  return flight_cmds

def getAltitudeReadings():
  """ Get current height from ground
  """
  return RoboCaller().call("getAltitudeReadings", "int")

def stopAllMotors():
  """ Sends a speed = 0 command to all motors. aeroLoopOff is a better
  way to kill

  """
  return RoboCaller().call("stopAllMotors", "void")

def maintainConnection():
  """ tells RoboVero that host is still here. If after 5 iterations of
  aeroLoop and no connection is maintained, RoboVero will automatically
  stop

  """
  return RoboCaller().call("maintainConnection", "void")

def setAngleLimit(angle_limit):
  """ Set the maximum angle before RoboVero shuts down the motors

  angle_limit: angle limit in degrees

  """
  return RoboCaller().call("setAngleLimit", "void", angle_limit)

def setTargetAltitude(altitude):
  """ Set target altitude to try to maintain

  """
  return RoboCaller().call("setTargetAltitude", "void", altitude)

def toggleAltitudeControl(toggle):
  """ Turns altitude control off if toggle = 0. Otherwise turns it on

  """
  return RoboCaller().call("toggleAltitudeControl", "void", toggle)

def changeMew(new_mew):
  """ changes the mew used in weighted average in balance filter.

  Found in aeroangle.c

  """
  return RoboCaller().call("changeMew", "void", new_mew*1000)

def setLowPassU(new_low_pass_u):
  """ Sets the low_pass_u found in aerodroid.c. Should be used for low
  pass filter on accelerometer readings. (currently not used)
  """
  return RoboCaller().call("setLowPassU", "void", new_low_pass_u * 1000)
