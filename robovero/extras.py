"""Defines public functions and classes not part of the CMSIS driver library.
"""

from robovero.internals import RoboCaller, cstruct, malloc, free, isr_list

__author__ =      "Neil MacMunn"
__email__ =        "neil@gumstix.com"
__copyright__ =   "Copyright 2010, Gumstix Inc."
__license__ =     "BSD 2-Clause"
__version__ =      "0.1"


class Array(object):
  """Allocates and initializes an array in RoboVero RAM.
  """
  def __init__(self, length, size, values=[]):
    """
    Args:
    
    - length(int): length of array
    - size(int): each item's size
    - values(list/int/str): 
      - list: try create array of the list
      - int: try create array with initial value of values
      - str: try create a string array 
    
    TODO: ensure the type of size
    
    """
    self.length = length
    self.size = size
    self.ptr = malloc(size * length)
    
    # assign the same value to all items
    if type(values) == int:
      for i in range(length):
        self[i] = values
    
    # copy a list of values
    elif type(values) == list:
      for i in range(min(length, len(values))):
        self[i] = values[i]
        
    # convert a string to a list of characters and copy
    elif type(values) == str:
      values = list(values)
      for i in range(min(length, len(values))):
        self[i] = ord(values[i])

  def __getitem__(self, key):
    """
    Return:
    
    - (int):value of Array[key]
    
    """
    if key >= self.length:
      raise IndexError
    return RoboCaller().call("deref", "int", self.ptr + self.size*key, self.size)

  def __setitem__(self, key, value):
    """
    Args:
    
    - key(int): the index of the item in the array
    - value(int): the value the item needs to set to
    
    """
    if key >= self.length:
      raise IndexError
    if type(value) != int:
      raise TypeError
    RoboCaller().call("deref", "void", self.ptr + self.size*key, self.size, value)
    
  def __del__(self):
    free(self.ptr)

def roboveroConfig():
  """Configure the microcontroller pin select registers according to the labels
  on the RoboVero board.
  """
  return RoboCaller().call("roboveroConfig", "void")
  
def heartbeatOn():
  """Flash the onboard LED.
  """
  return RoboCaller().call("heartbeatOn", "void")
  
def heartbeatOff():
  """Let user control the onboard LED.
  """
  return RoboCaller().call("heartbeatOff", "void")

def initMatch(ch, count):
  """Initialize a PWM match condition.
  """
  return RoboCaller().call("initMatch", "void", ch, count)
  
def registerCallback(IRQn, function):
  """Register a RoboVero interrupt service routine.
  
  Args:
  
  - IRQn(int): Interrupt number
  - function(function): A pointer to the function that is called when an interrupt occurs
  
  """
  isr_list[IRQn] = function
