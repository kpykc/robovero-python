from robovero.aero_internals import *
from robovero.extras import roboveroConfig, heartbeatOn, heartbeatOff
from robovero.lpc17xx_pwm import PWM_MatchUpdate, PWM_MATCH_UPDATE_OPT
from robovero.lpc17xx_i2c import I2C_M_SETUP_Type
from robovero.LPC17xx import LPC_PWM1
from robovero.cr_dsplib import *
from time import sleep

import sys    
import termios
import fcntl
import os
import atexit

""" TODO:
Use IMU specific functions
Add Yaw correction
"""

throttle = 1500

LIMIT_ANGLE = 20
ANGLE_RESTORE = 5
ACCEL_LIMIT = 1200
SCALE_LEVEL_PID = 1 
SCALE_LEVEL_GYRO_PID = 180

def setPID():
  setLevelRollPID (3.5 *SCALE_LEVEL_PID, 0 *SCALE_LEVEL_PID,0 *SCALE_LEVEL_PID)  # 3.5, 0, 0 
  setLevelPitchPID(3.5 *SCALE_LEVEL_PID, 0 *SCALE_LEVEL_PID,0 *SCALE_LEVEL_PID)
  setLevelGyroRollPID (.149 *SCALE_LEVEL_GYRO_PID, 0.039 *SCALE_LEVEL_GYRO_PID, -.01 *SCALE_LEVEL_GYRO_PID) # .149, .039. -.01
  setLevelGyroPitchPID(.149 *SCALE_LEVEL_GYRO_PID, 0.039 *SCALE_LEVEL_GYRO_PID, -.01 *SCALE_LEVEL_GYRO_PID)

def dontCrash():
  angles = getFlightAngles()
  accel = getAccelReadings()
  global throttle
  
  for i in range(len(angles)-1):
    if (abs(angles[i]) > LIMIT_ANGLE):
      print "angle limit reached"
      throttle=1250
      setThrottle(throttle)
      angles = getFlightAngles()
      while (abs(angles[i]) > ANGLE_RESTORE):
        angles = getFlightAngles()
        print angles
        sleep(0.25)
      print "restabilized"
      setPID()
      sleep(1.5)
    
  if (abs(accel[2]) > ACCEL_LIMIT):
    print "accel limit reached"
    throttle=1250
    setThrottle(throttle)
    accel = getAccelReadings()
    while (abs(accel[2]) > ACCEL_LIMIT):
      accel = getAccelReadings()
      print accel
      sleep(0.25)
    print "restabilized"
    setPID()
    sleep(1.5)
  
def printData():
  print getMotorCommands(), getFlightAngles(), getFlightCmds()
"""  
def myGetch():
    fd = sys.stdin.fileno()

    oldterm = termios.tcgetattr(fd)
    newattr = termios.tcgetattr(fd)
    newattr[3] = newattr[3] & ~termios.ICANON & ~termios.ECHO
    termios.tcsetattr(fd, termios.TCSANOW, newattr)

    oldflags = fcntl.fcntl(fd, fcntl.F_GETFL)
    fcntl.fcntl(fd, fcntl.F_SETFL, oldflags | os.O_NONBLOCK)

    try:        
        while 1:            
            try:
                c = sys.stdin.read(1)
                break
            except IOError: pass
            dontCrash()
            printData()
            sleep(0.25)
    finally:
        termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)
        fcntl.fcntl(fd, fcntl.F_SETFL, oldflags)
        return c
"""

#roboveroConfig()

aeroInit()
setPID()

heartbeatOff()
aeroLoopOn()

setThrottle(throttle)

try:
  while True:
    """
    s=myGetch()
    if (s=='w'):
      throttle=throttle+25
    elif (s=='s'):
      throttle=throttle-25
    else:
      throttle=1250
    setThrottle(throttle)
    """
    printData()
    throttle += 1
    if (throttle > 1500):
      throttle=1500
    setThrottle(throttle)
    for i in range(throttle/500):
      dontCrash()
      sleep(0.02)
    #sleep(.1)
except:
  aeroLoopOff()
  heartbeatOn()
  #stopAllMotors()
