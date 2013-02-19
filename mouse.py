from IMU2 import IMU, Vector3D
from os import system
from PyMouse.pymouse import PyMouse

''' This contains definition of
    mouse actions'''
class MouseAction(object):
  def __init__(self):
    self.mouse = PyMouse()

  def single_click(self, valid_call):
    if not valid_call:
      return
    # TODO: Single click
    pass

  def double_click(self, valid_call):
    if not valid_call:
      return
    # TODO: Double click
    pass

  def move(self, xyz):
    if not xyz:
      return
    current_position = list(self.mouse.position())
    current_position.append(0)
    current_position = Vector3D(current_position)

    target = current_position + xyz
    print current_position, target

    print 'move to ' + str([target.x, target.y])
    self.mouse.move(target.x, target.y)


''' This will determine if one action
    is triggered or not '''
class ActionTrigger(object):
  def __init__(self):
    self.imu = IMU()
    self.action = MouseAction()
    # how much does robo's position change will move the mouse

    self.LIMIT = Vector3D([5, 5, 5])

  ''' Check if there is any position
      change that could be a mouse action '''
  def monitor(self):
    print 'Monitoring'
    self.action.move(self.get_mouse_move_value())
    self.action.single_click(self.get_single_click_value())
    self.action.double_click(self.get_double_click_value())

  def get_mouse_move_value(self):
    xyz = self.imu.gyrometer.xyz
    # Do not trigger if less than threshold
    if abs(xyz.x) < self.LIMIT.x:
      xyz.x = 0
    if abs(xyz.y) < self.LIMIT.y:
      xyz.y = 0
    if abs(xyz.z) < self.LIMIT.z:
      xyz.z = 0
    return xyz

  def get_single_click_value(self):
    ret = False
    if ret:
      print 'Single Click'
    return ret

  def get_double_click_value(self):
    ret = False
    if ret:
      'Double Click'
    return ret


if __name__ == "__main__":
  trigger = ActionTrigger()
  while True:
    trigger.monitor()
