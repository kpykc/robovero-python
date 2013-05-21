from robovero.extras import roboveroConfig
from robovero.internals import RoboCaller


def getServoAngle():
	"""Get an angle from the user and calculate new duty cycle.
	"""
	user_angle = raw_input("New angle: ")
	return int(user_angle)


def run():
  roboveroConfig()
  r = RoboCaller()
  r.call('PWM_SetBasePeriod', 'void', 2000)
  r.call('PWM_SetSpeed', 'void', 1, 10)
  while True:
    match_value = getServoAngle()
    if match_value:
      r.call('PWM_SetSpeed', 'void', 1, match_value)


if __name__ == '__main__':
  run()