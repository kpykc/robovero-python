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
            [m1, m2, m3, m4]=getMotorCommands()
            print [m1, m2, m3, m4]
            sleep(0.25)
    finally:
        termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)
        fcntl.fcntl(fd, fcntl.F_SETFL, oldflags)
        return c

#roboveroConfig()
accelerometer=I2C_M_SETUP_Type()
gyro = I2C_M_SETUP_Type()

aeroInit(accelerometer.ptr, gyro.ptr)

heartbeatOff()
aeroLoopOn()

throttle=1250

setThrottle(throttle)

try:
  while True:
    c=myGetch()
    if (c=='w'):
      throttle=throttle+25
    elif (c=='s'):
      throttle=throttle-25
    else:
      throttle=1250
    setThrottle(throttle)
    #pass
except KeyboardInterrupt:
  aeroLoopOff()
  heartbeatOn()
  #stopAllMotors()
