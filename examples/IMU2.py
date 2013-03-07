"""Example application that outputs accelerometer, compass and gyro readings.
"""

from robovero.extras import Array, roboveroConfig
from robovero.arduino import pinMode, digitalWrite, P1_0, OUTPUT
from robovero.lpc17xx_i2c import I2C_M_SETUP_Type, I2C_MasterTransferData, \
    I2C_TRANSFER_OPT_Type
from robovero.lpc17xx_gpio import GPIO_ReadValue
from robovero.LPC17xx import LPC_I2C0
from robovero.lpc_types import Status
from time import sleep

__author__ =      ["Neil MacMunn", "Danny Chan"]
__email__ =       "neil@gumstix.com"
__copyright__ =   "Copyright 2012, Gumstix Inc"
__license__ =     "BSD 2-Clause"
__version__ =     "0.1"


def twosComplement(low_byte, high_byte):
  """Unpack 16-bit twos complement representation of the result.
  """
  return (((low_byte + (high_byte << 8)) + 2**15) % 2**16 - 2**15)


class Vector3D(object):
  def __init__(self, data):
    if type(data) is not list:
      data = list(data)
    self.x = data[0]
    self.y = data[1]
    self.z = data[2]

  def __add__(self, other):
    x = self.x + other.x
    y = self.y + other.y
    z = self.z + other.z
    return Vector3D([x, y, z])

  def __sub__(self, other):
    x = self.x - other.x
    y = self.y - other.y
    z = self.z - other.z
    return Vector3D([x, y, z])

  def __mul__(self, other):
    x = self.x * other.x
    y = self.y * other.y
    z = self.z * other.z
    return Vector3D([x, y, z])

  def __str__(self):
    return str([self.x, self.y, self.z])


class I2CDevice(object):
  def __init__(self, address):
    self.config = I2C_M_SETUP_Type()
    self.tx_data = Array(2, 1)
    self.rx_data = Array(1, 1)
    self.rx_data6 = Array(6, 1)
    self.config.sl_addr7bit = address
    self.config.tx_data = self.tx_data.ptr
    self.config.retransmissions_max = 3

  def readReg(self, register):
    self.tx_data[0] = register
    self.config.tx_length = 1
    self.config.rx_data = self.rx_data.ptr
    self.config.rx_length = 1
    ret = I2C_MasterTransferData(LPC_I2C0, self.config.ptr,
                                  I2C_TRANSFER_OPT_Type.I2C_TRANSFER_POLLING)
    if ret == Status.ERROR:
      exit("I2C Read Error")
    return self.rx_data[0]

  def read6Reg(self, register):
    #MSB must be equal to 1 to read multiple bytes
    self.tx_data[0] = register | 0b10000000
    self.config.tx_length = 1
    self.config.rx_data = self.rx_data6.ptr
    self.config.rx_length = 6
    ret = I2C_MasterTransferData(LPC_I2C0, self.config.ptr,
                                  I2C_TRANSFER_OPT_Type.I2C_TRANSFER_POLLING)
    if ret == Status.ERROR:
      exit("I2C Read Error")
    return self.rx_data6

  def writeReg(self, register, value):
    self.tx_data[0] = register
    self.tx_data[1] = value
    self.config.tx_length = 2
    self.config.rx_data = 0
    self.config.rx_length = 0
    ret = I2C_MasterTransferData(LPC_I2C0, self.config.ptr,
                                  I2C_TRANSFER_OPT_Type.I2C_TRANSFER_POLLING)
    if ret == Status.ERROR:
      exit("I2C Write Error")
    if self.readReg(register) != value:
      exit("I2C Verification Error")
    return None

class IMUDevice(I2CDevice):
  def __init__(self, i2c_addr):
    self.i2c_addr = i2c_addr

    self.low = Vector3D([0x0, 0x0, 0x0])
    self.high = Vector3D([0x0, 0x0, 0x0])

    # Offset and gain is used
    # for caliberation purpose
    self.offset = Vector3D([0, 0, 0])
    self.gain = Vector3D([1, 1, 1])

    super(IMUDevice, self).__init__(self.i2c_addr)
    self.read_6_reg = self.low.x

  def get_readings(self):
    if not self.read_6_reg:
      self.read_6_reg = self.low.x
    data = self.read6Reg(self.read_6_reg)

    self.low.x = data[0]
    self.high.x = data[1]
    self.low.y = data[2]
    self.high.y = data[3]
    self.low.z = data[4]
    self.high.z = data[5]

    x = twosComplement(self.low.x, self.high.x)
    y = twosComplement(self.low.y, self.high.y)
    z = twosComplement(self.low.z, self.high.z)

    readings = Vector3D([x, y, z])
    readings = (readings - self.offset) * self.gain
    return readings

  @property
  def xyz(self):
    return self.get_readings()

  @property
  def x(self):
    return self.xyz.x

  @property
  def y(self):
    return self.xyz.y

  @property
  def z(self):
    return self.xyz.z


class Accelerometer(IMUDevice):
  def __init__(self):
    self.i2c_addr = 0x18
    self.ctrl_reg1 = 0x20
    self.ctrl_reg4 = 0x23

    super(Accelerometer, self).__init__(self.i2c_addr)
    self.writeReg(self.ctrl_reg1, 0x27)
    self.writeReg(self.ctrl_reg4, 0x00)

    self.low = Vector3D([0x28, 0x2A, 0x2C])
    self.high = Vector3D([0x29, 0x2B, 0x2D])

    self.offset = Vector3D([0, 0, 0])
    self.gain = Vector3D([1/16384.0, 1/16384.0, 1/16384.0])


class Compass(IMUDevice):
  def __init__(self):
    self.i2c_addr = 0x1E
    self.cra_reg = 0x00
    self.crb_reg = 0x01
    self.mr_reg = 0x02

    super(Compass, self).__init__(self.i2c_addr)
    self.writeReg(self.cra_reg, 0x18) # 75 Hz
    self.writeReg(self.crb_reg, 0x20) # +/- 1.3 gauss
    self.writeReg(self.mr_reg, 0) # continuous measurement mode

    self.low = Vector3D([0x4, 0x6, 0x8])
    self.high = Vector3D([0x3, 0x5, 0x7])

    self.offset = Vector3D([0, 0, 0])
    self.gain = Vector3D([1/1055.0, 1/1055.0, 11/950.0])

    self.read_6_reg = self.high.x


class Gyrometer(IMUDevice):
  def __init__(self):
    self.i2c_addr = 0x68
    self.ctrl_reg1 = 0x20
    self.ctrl_reg2 = 0x21
    self.ctrl_reg3 = 0x22
    self.ctrl_reg4 = 0x23
    self.ctrl_reg5 = 0x24
    self.status_reg = 0x27
    self.fifo_ctrl_reg = 0x2E

    super(Gyrometer, self).__init__(self.i2c_addr)
    self.writeReg(self.ctrl_reg1, 0x0F) # normal mode, enable all axes, 250dps
    self.writeReg(self.ctrl_reg3, 0x08) # enable DRDY
    self.writeReg(self.ctrl_reg4, 0x80) # enable block data read mode

    self.low = Vector3D([0x28, 0x2A, 0x2C])
    self.high = Vector3D([0x29, 0x2B, 0x2D])

    self.offset = Vector3D([0, 0, 0])
    self.gain = Vector3D([0.0085, 0.0085, 0.0085])


class IMU(object):
  def __init__(self):
    # Initialize pin select registers
    roboveroConfig()
    # enable IMU_EN
    pinMode(P1_0, OUTPUT)
    digitalWrite(P1_0, 0)
    self.accelerometer = Accelerometer()
    self.compass = Compass()
    self.gyrometer = Gyrometer()

def print_IMU():
  imu = IMU()

  while True:
    #print "time: ",
    #print time.time()

    #print "a [x, y, z]: ",
    #print [
      #imu.accelerometer.x,
      #imu.accelerometer.y,
      #imu.accelerometer.z
    #]

    #print "c [x, y, z]: ",
    #print [
      #imu.compass.x,
      #imu.compass.y,
      #imu.compass.z
    #]

    xyz = imu.gyrometer.xyz
    print "g [x, y, z]: ",
    print [
      xyz.x,
      xyz.y,
      xyz.z
    ]
    sleep(0.1)

if __name__ == '__main__':
  printIMU()
