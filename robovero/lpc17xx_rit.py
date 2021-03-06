"""Repetitive interrupt timer client library functions. Find implementation 
details in LPC17xx CMSIS-Compliant Standard Peripheral Firmware Driver Library 
documentation."""

from internals import RoboCaller, cstruct
from lpc_types import _BIT

__author__ =      "Neil MacMunn"
__credits__ =     ["Neil MacMunn", "NXP MCU SW Application Team"]
__maintainer__ =  "Neil MacMunn"
__email__ =       "neil@gumstix.com"
__copyright__ =   "Copyright 2011, Gumstix Inc"
__license__ =     "BSD 2-Clause"
__version__ =     "0.1"

def RIT_DeInit(RITx):
  '''Deinitialize RIT.
  
  - Turn off power and clock
  - Reset default register values
  
  Args:
  
  - RITx: peripheral selected, should be: LPC_RIT
  
  '''
  return RoboCaller().call("RIT_DeInit", "void", RITx)

def RIT_Init(RITx):
  '''Initialize RIT.
  
  - Turn on power and clock
  - Setup default register values
  
  Args:
  
  - RITx: peripheral selected, should be: LPC_RIT
  
  '''
  return RoboCaller().call("RIT_Init", "void", RITx)

def RIT_Cmd(RITx, NewState):
  '''Enable/Disable Timer.
  
  Args:
  
  - RITx: peripheral selected, should be: LPC_RIT
  - NewState   New state of this function:

    - ENABLE: Enable Timer
    - DISABLE: Disable Timer
        
  '''
  return RoboCaller().call("RIT_Cmd", "void", RITx, NewState)

def RIT_GetIntStatus(RITx):
  '''Check whether interrupt flag is set or not.
  
  Args:
  
  - RITx: peripheral selected, should be: LPC_RIT
  
  Return: 
  
  - Current interrupt status, could be: SET/RESET
  
  '''
  return RoboCaller().call("RIT_GetIntStatus", "IntStatus", RITx)

def RIT_TimerConfig(RITx, time_interval):
  '''Set compare value, mask value and time counter value.
  
  Args:
  
  - RITx: peripheral selected, should be: LPC_RIT
  - time_interval:  timer interval value (ms)
  
  '''
  return RoboCaller().call("RIT_TimerConfig", "void", RITx, time_interval)

def RIT_TimerDebugCmd(RITx, NewState):
  '''Timer Enable/Disable on debug.
  
  Args:
  
  - RITx: peripheral selected, should be: LPC_RIT
  - NewState: New State of this function
    
    -ENABLE: The timer is halted whenever a hardware break condition occurs
    -DISABLE: Hardware break has no effect on the timer operation
  
  '''
  return RoboCaller().call("RIT_TimerDebugCmd", "void", RITx, NewState)
