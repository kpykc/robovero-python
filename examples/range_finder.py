"""Example demonstrating use of HC-SR04 Ultrasonic Rangefinder.
Requires updated firmware for microsecond pulse
"""

from robovero.arduino import pinMode, P0_4, P0_5, INPUT, OUTPUT, pulseIn
from time import sleep

__author__ =			"Danny Chan"
__email__ =				"danny@gumstix.com"
__copyright__ = 	"Copyright 2012, Gumstix Inc"
__license__ = 		"BSD 2-Clause"
__version__ =			"0.1"


def run():
  echo_pin = P0_5
  trig_pin = P0_4

  pinMode(trig_pin,OUTPUT)
  pinMode(echo_pin,INPUT)

  try:
    while True:
      print pulseIn(trig_pin, echo_pin, 9850)/58 # cm. Divide by 148 for in.
      sleep(.1)
  except:
    print "goodbye"
