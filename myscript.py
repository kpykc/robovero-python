from robovero.script import Script
from time import sleep

from robovero.extras import roboveroConfig, initMatch, heartbeatOff, heartbeatOn
from robovero.lpc_types import FunctionalState

from robovero.arduino import analogWrite, PWM1, pinMode, OUTPUT, LED

__author__ =			"Neil MacMunn"
__email__ =				"neil@gumstix.com"
__copyright__ = 	"Copyright 2010, Gumstix Inc"
__license__ = 		"BSD 2-Clause"
__version__ =			"0.1"

roboveroConfig()
pinMode(LED, OUTPUT)
heartbeatOff()

myscript=Script([["GPIO_ClearValue", 3, 2000000],
  ["delay",10000000],
  ["GPIO_SetValue", 3, 2000000]])
print "script added"

try:
  while True:
    raw_input("Press Enter to run script")
    print myscript.run()
    print "script done"
    myscript.append("delay",10000000)
    myscript.append("GPIO_ClearValue", 3, 2000000)
    myscript.append("delay",10000000)
    myscript.append("GPIO_SetValue",3, 2000000)
except:
  heartbeatOn()
  print "goodbye"
