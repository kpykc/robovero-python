"""Watchdog client library functions. Find implementation details in  LPC17xx
CMSIS-Compliant Standard Peripheral Firmware Driver Library documentation.
"""

from internals import RoboCaller

__author__ =      "Neil MacMunn"
__credits__ =     ["Neil MacMunn", "NXP MCU SW Application Team"]
__maintainer__ =  "Neil MacMunn"
__email__ =       "neil@gumstix.com"
__copyright__ =   "Copyright 2011, Gumstix Inc"
__license__ =     "BSD 2-Clause"
__version__ =     "0.1"

class WDT_MODE_OPT:
  '''WDT operation mode.
  
  - WDT_MODE_INT_ONLY:  Use WDT to generate interrupt only
  - WDT_MODE_RESET: Use WDT to generate interrupt and reset MCU
  
  '''
  WDT_MODE_INT_ONLY = 0
  WDT_MODE_RESET = 1

class WDT_CLK_OPT:
  '''Clock source option for WDT.
  
  - WDT_CLKSRC_IRC0:  Clock source from Internal RC oscillator
  - WDT_CLKSRC_PCLK:  Selects the APB peripheral clock (PCLK
  - WDT_CLKSRC_RTC: Selects the RTC oscillator
   
  '''
  WDT_CLKSRC_IRC = 0
  WDT_CLKSRC_PCLK = 1
  WDT_CLKSRC_RTC = 2

def WDT_Start(TimeOut):
  '''Start WDT activity with given timeout value.
  
  Args:
  
  - TimeOut:  WDT reset after timeout if it is not feed
  
  '''
  return RoboCaller().call("WDT_Start", "void", TimeOut)

def WDT_ClrTimeOutFlag():
  '''Clear WDT timeout flag.
  '''
  return RoboCaller().call("WDT_ClrTimeOutFlag", "void")

def WDT_ReadTimeOutFlag():
  '''Read WDT timeout flag.
  
  Return: 
  
  - timeout flag status of WDT
  
  '''
  return RoboCaller().call("WDT_ReadTimeOutFlag", "FlagStatus")

def WDT_UpdateTimeOut(TimeOut):
  '''Update WDT timeout value and feed.
  
  Args:
   
   - TimeOut:  timeout value to be updated
  
  '''
  return RoboCaller().call("WDT_UpdateTimeOut", "void", TimeOut)

def WDT_Init(ClkSrc, WDTMode):
  '''Initialize the Watchdog timer function.
  
  Args:
  
  - ClkSrc: Select clock source, should be:

    - WDT_CLKSRC_IRC: Clock source from Internal RC oscillator
    - WDT_CLKSRC_PCLK: Selects the APB peripheral clock (PCLK)
    - WDT_CLKSRC_RTC: Selects the RTC oscillator

  - WDTMode:  WDT mode, should be:

    - WDT_MODE_INT_ONLY: Use WDT to generate interrupt only
    - WDT_MODE_RESET: Use WDT to generate interrupt and reset MCU

  '''
  return RoboCaller().call("WDT_Init", "void", ClkSrc, WDTMode)

def WDT_Feed():
  '''After setting WDTEN, call this function to start Watchdog or reload the 
  Watchdog timer.
  '''
  return RoboCaller().call("WDT_Feed", "void")

def WDT_GetCurrentCount():
  '''Get the current value of WDT.
  
  Return: 
  
  - current value of WDT
  
  '''
  return RoboCaller().call("WDT_GetCurrentCount", "uint32_t")
