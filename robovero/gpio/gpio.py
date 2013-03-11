""" This is a trail run for converting a gpio pin
  into an object that can be easily used. And this
  should speed up the development process.
"""

from robovero.internals import RoboCaller

INPUT = 0
OUTPUT = 1

class GPIOPin(object):
  def __init__(self, port, pin):
    """
    Args:
    
    - port(int): the port number of the pin
    - pin(int): the pin number of the pin
    
    """
    
    self.port = port
    self.pin = pin
    self.half_word = False
  
  def interrupt(self, interrupt):
    pass
    self.interrrupt = interrupt
    
  def set_direction(self, direction):
    """Set the direction for the gpio"""
    try:
      if direction in [INPUT, OUTPUT]:
        return RoboCaller().call("GPIO_SetDir", "void", self.port, 1 << self.pin, direction)
      else:
        raise ValueError
    except ValueError, err:
      print "Pin direction can only be 0/1, INPUT/OUTPUT"
    
  def read(self):
    """Read the value from gpio"""
    read_byte = RoboCaller().call("GPIO_ReadValue", "uint32_t", self.port)
    gpio_mask = (1 << self.pin)
    
    gpio_value = read_byte & gpio_mask
    
    if gpio_value:
      return 1
    else:
      return 0

  def write(self, value):
    """Write bit or byte to the gpio
    
    Args:
    
    - Value: value to gpio, 1 or 0
      
    """
    try:
      if value == 1:
        RoboCaller().call("GPIO_SetValue", "void", self.port, 1 << self.pin)
      elif value == 0:
        RoboCaller().call("GPIO_ClearValue", "void", self.port, 1 << self.pin)
      else:
        raise ValueError
    except ValueError, err:
      print 'You can only write 1 or 0 to a GPIO pin'
  
  def set_mask(self, mask):
    pass

  def set_half_word_mode(self, status):
    pass
