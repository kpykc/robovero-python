''' Use to lauch robovero example, need ttyACM0 to be robovero
'''
import sys
from examples import IMU2, adc

EXAMPLES=[
  'IMU',
  'ADC',
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
    IMU2.run()
  elif example_id is 1:
    print 'call adc'
    adc.run()


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
