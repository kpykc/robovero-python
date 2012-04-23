""" Handles scripting for RoboVero
"""

from internals import robocaller, getIndex, getReturn, getStatus

__author__ =      "Danny Chan"
__email__ =        "danny@gumstix.com"
__copyright__ =   "Copyright 2012, Gumstix Inc."
__license__ =     "BSD 2-Clause"
__version__ =      "0.1"

class Script(object):
  """Allocates and initializes an script in RoboVero RAM.
  """
  def __init__(self, cmds=[]):
    self.ptr = robocaller("scriptInit", "int")
    self.length = 0
    self.cmd_list = []
      
    # copy a list of values
    if type(cmds) == list:
      for i in range(len(cmds)):
        self.append(cmds[i])
        
  """def __getitem__(self, key):
    if key >= self.length:
      raise IndexError
    return robocaller("deref", "int", self.ptr + self.size*key, self.size)

  def __setitem__(self, key, value):
    if key >= self.length:
      raise IndexError
    if type(value) != int:
      raise TypeError
    robocaller("deref", "void", self.ptr + self.size*key, self.size, value)
  """
  
  def append(self, *cmds):
    # check if passed as a list
    if len(cmds) == 1:
      cmds = cmds[0]
    
    fcn = getIndex(cmds[0])
    args=""
    if (len(cmds) > 1):
      args = str(cmds[1])
      for j in range(2, len(cmds)):
        args += " " + str(cmds[j])
    self.length += 1
    self.cmd_list.append(cmds[0])
    robocaller("scriptAdd", "void", self.ptr, fcn, args)
    
  def run(self):
    robocaller("scriptRun", "void", self.ptr)
    script_return = getReturn()
    while ("script_done" not in script_return) and ("script_fail" not in script_return):
      print script_return
      script_return = getReturn()
    if ("script_fail" in script_return):
      failed_function = getReturn()
      return self.cmd_list[failed_function]
    return 0
    
  def __del__(self):
    robocaller("scriptDel", "void", self.ptr)
