from robovero.extras import roboveroConfig
from robovero.internals import RoboCaller

def getServoAngle():
	"""Get an angle from the user and calculate new duty cycle.
	"""
	user_angle = raw_input("New angle: ")
	return user_angle

def run():
  roboveroConfig()
  RoboCaller.call('PWM_SetBasePeriod', 'void', 2000)
  RoboCaller.call('PWM_SetSpeed', 'void', 1, 10)
  while True:
    match_value = getServoAngle()
    if match_value:
      RoboCaller.call('PWM_SetSpeed', 'void', 1, match_value)
