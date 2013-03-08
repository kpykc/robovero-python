''' Use to lauch robovero example, need ttyACM0 to be robovero
'''
import sys
from examples import \
  IMU,\
  adc,\
  callback,\
  can_recv,\
  can_send,\
  clockout,\
  DSP,\
  gpio,\
  mcpwm,\
  piezo,\
  servo,\
  stepper,\
  uart_recv,\
  uart_send

EXAMPLES=[
  'IMU',
  'adc',
  'callback',
  'can_recv',
  'can_send',
  'clockout',
  'DSP',
  'gpio',
  'mcpwm',
  'piezo',
  'servo',
  'stepper',
  'uart_recv',
  'uart_send',
]

def parse_argv(argv):
  command = None
  option = None
  try:
    command = str(argv[1])
    option = str(argv[2])
  except:
    pass

  if command == 'run':
    run_example(option)
  elif command == 'list':
    list_examples()
  else:
    help()
  exit()


def run_example(example):
  example_id = -1
  if not example:
    print 'Please provide an example, type help for details'
    return
  elif example.isdigit():
    example_id = int(example)
  elif example in EXAMPLES:
    example_id = EXAMPLES.index(example)
  else:
    print '''Can't find example'''
    return

  if example_id is 0:
    print 'call IMU'
    IMU.run()
  elif example_id is 1:
    print 'call adc'
    adc.run()
  elif example_id is 2:
    callback.run()
  elif example_id is 3:
    can_recv.run()
  elif example_id is 4:
    can_send.run()
  elif example_id is 5:
    clockout.run()
  elif example_id is 6:
    DSP.run()
  elif example_id is 7:
    gpio.run()
  elif example_id is 8:
    mcpwm.run()
  elif example_id is 9:
    piezo.run()
  elif example_id is 10:
    servo.run()
  elif example_id is 11:
    stepper.run()
  elif example_id is 12:
    uart_recv.run()
  elif example_id is 13:
    uart_send.run()

def list_examples():
  for i in range(len(EXAMPLES)):
    example_id = str(i)
    example_name = EXAMPLES[i]
    print example_id, example_name


def help():
  help_text = '''\
  Options:
    list -- Show a list of examples
    run NAME_OF_EXAMPLE -- Run example by name
    run ID_OF_EXAMPLE -- Run example by id
    help -- Show this help\
  '''
  print help_text


if __name__ == '__main__':
  argv = sys.argv
  parse_argv(argv)
