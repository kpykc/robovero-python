from robovero.aero_internals import *
from robovero.extras import roboveroConfig, heartbeatOn, heartbeatOff
from robovero.lpc17xx_pwm import PWM_MatchUpdate, PWM_MATCH_UPDATE_OPT
from robovero.lpc17xx_i2c import I2C_M_SETUP_Type
from robovero.LPC17xx import LPC_PWM1
from robovero.cr_dsplib import *
from time import sleep, time

import csv

import sys    
import termios
import fcntl
import os

writer = csv.writer(open('data.csv', 'wb'), delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)

MEW = 0.1
LOW_PASS_U = 0.1

LIMIT_ANGLE = 15
TARGET_ALTITUDE = 15
ALTITUDE_CONTROL = 0
ANGLE_RESTORE = 5
ACCEL_LIMIT = 2500
P1 = 3.5 * 30
P2 = 2.5

I1 = 5
I2 = 0

D1 = 0
D2 = 0

SCALE_LEVEL_PID = 30 
SCALE_LEVEL_GYRO_PID = 15
INIT_THROTTLE = 1400 
TAKE_OFF_LIMIT=1550

def setPID():
  setLevelRollPID ( P1 , I1, D1)  # 3.5, 0, 0 
  setLevelPitchPID(-P1 , -I1, D1)
  setLevelGyroRollPID (P2, I2, D2) # .149, .039. -.01
  setLevelGyroPitchPID(-P2, -I2, D2)
  setAltitudePID(.1, 0.02, 0) #0.4, 0.02, 0

def dontCrash():
  angles = getFlightAngles()
  accel = getAccelReadings()
  global throttle
  
  for i in range(len(angles)-1):
    if (abs(angles[i]) > LIMIT_ANGLE):
      logData(0)
      aeroLoopOff()
      no_error = False
      print "angle limit reached"
      """throttle=1000
      setThrottle(throttle)
      stopAllMotors()
      angles = getFlightAngles()
      while (abs(angles[i]) > ANGLE_RESTORE):
        angles = getFlightAngles()
        print angles
        logData(0)
        maintainConnection()
        sleep(0.02)

      print "restabilized"
      setPID()
      
      for x in range(75):
        sleep(0.02)
        maintainConnection()"""
    
  if (abs(accel[2]) > ACCEL_LIMIT):
    print "accel limit reached"
    logData(0)
    throttle=1000
    setThrottle(throttle)
    stopAllMotors()
    accel = getAccelReadings()
    aeroLoopOff()
    
    """while (abs(accel[2]) > ACCEL_LIMIT):
      accel = getAccelReadings()
      print accel
      logData(0)
      maintainConnection()
      sleep(0.02)
      
    print "restabilized"
    setPID()
    
    for x in range(75):
      sleep(0.02)
      maintainConnection()
      
  armMotors()"""
  
def logData(show_on_screen):
  data = [getMotorCommands()]
  maintainConnection()
  data.append(getFlightAngles())
  maintainConnection()
  #data.append(getBalanceAngles())
  #maintainConnection()
  data.append(getFlightCmds())
  maintainConnection()
  data.append(getAccelReadings())
  maintainConnection()
  data.append(getGyroReadings())
  maintainConnection()
  data.append(getAltitudeReadings())
  maintainConnection()
  if (show_on_screen):
    print data[0], data[1], data[2]
  writer.writerow(data)
  
def myGetch():
  fd = sys.stdin.fileno()

  oldterm = termios.tcgetattr(fd)
  newattr = termios.tcgetattr(fd)
  newattr[3] = newattr[3] & ~termios.ICANON & ~termios.ECHO
  termios.tcsetattr(fd, termios.TCSANOW, newattr)

  oldflags = fcntl.fcntl(fd, fcntl.F_GETFL)
  fcntl.fcntl(fd, fcntl.F_SETFL, oldflags | os.O_NONBLOCK)
  
  c=''

  try:        
    try:
      c = sys.stdin.read(1)
    except IOError: pass
  finally:
    termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)
    fcntl.fcntl(fd, fcntl.F_SETFL, oldflags)
    return c

#roboveroConfig()

heartbeatOff()
aeroInit()
setPID()
setAngleLimit(LIMIT_ANGLE)
toggleAltitudeControl(ALTITUDE_CONTROL)
setTargetAltitude(TARGET_ALTITUDE)
changeMew(MEW)
setLowPassU(LOW_PASS_U)
maintainConnection()

writer.writerow([P1, P2, I1, I2, D1, D2])

aeroLoopOn()

setThrottle(INIT_THROTTLE)
maintainConnection()

throttle = INIT_THROTTLE
count = 0

try:
  while True:
    maintainConnection()
    logData(1)
    maintainConnection()
    c=myGetch()
    maintainConnection()
    if c=='s':
      throttle += 3
      #~ count = 50
    
      if (throttle > TAKE_OFF_LIMIT):
        throttle = TAKE_OFF_LIMIT
        
      setThrottle(throttle)
    elif c=='a':
      #count -= 1
      throttle -=3
      #~ if count<=0:
        #~ throttle -= 1
    
      if (throttle < INIT_THROTTLE):
        throttle = INIT_THROTTLE
          
      setThrottle(throttle)
    elif c=='':
      pass
    else:
      print "killed by key press"
      aeroLoopOff()
      exit()
          
    maintainConnection()
    
    """for i in range((throttle/500)*(throttle/500)):
      dontCrash()
      logData(0)
      #sleep(0.02)
      maintainConnection()"""

except:
  print "killed due to exception"
  aeroLoopOff()
