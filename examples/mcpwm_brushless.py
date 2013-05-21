"""BLDC control using MCPWM pins of the RoboVero.
See NXP Application note AN10898 for details on wiring and circuitry
"""

from robovero.lpc17xx_mcpwm import MCPWM_Init, MCPWM_CHANNEL_CFG_Type, \
                      MCPWM_ConfigChannel, MCPWM_DCMode, MCPWM_ACMode, \
                      MCPWM_Start, MCPWM_WriteToShadow, MCPWM_Stop,    \
                      MCPWM_CHANNEL_EDGE_MODE, MCPWM_CHANNEL_PASSIVE_LO,\
                      MCPWM_PATENT_A0, MCPWM_PATENT_A1, MCPWM_PATENT_A2,\
                      MCPWM_PATENT_B0, MCPWM_PATENT_B1, MCPWM_PATENT_B2
from robovero.extras import roboveroConfig
from robovero.LPC17xx import LPC_MCPWM
from robovero.lpc_types import FunctionalState
from robovero.extras import heartbeatOff, heartbeatOn
from time import sleep

__author__ =      "Danny Chan"
__email__ =       "danny@gumstix.com"
__copyright__ =   "Copyright 2012, Gumstix Inc."
__license__ =     "BSD 2-Clause"


def BLDC_commutate(step):
  if step == 0:
    pattern = MCPWM_PATENT_A0 | MCPWM_PATENT_B1
  elif step == 1:
    pattern = MCPWM_PATENT_B1 | MCPWM_PATENT_A2
  elif step == 2:
    pattern = MCPWM_PATENT_B0 | MCPWM_PATENT_A2
  elif step == 3:
    pattern = MCPWM_PATENT_B0 | MCPWM_PATENT_A1
  elif step == 4:
    pattern = MCPWM_PATENT_A1 | MCPWM_PATENT_B2
  elif step == 5:
    pattern = MCPWM_PATENT_A0 | MCPWM_PATENT_B2
  else:
    pattern = 0

  MCPWM_DCMode(LPC_MCPWM, FunctionalState.ENABLE, FunctionalState.DISABLE, pattern)

def run():
  heartbeatOff();
  roboveroConfig()

  MCPWM_Init(LPC_MCPWM)

  channelsetup=[]
  for i in range(3):
    channelsetup.append(MCPWM_CHANNEL_CFG_Type())

  channelsetup[0].channelType = MCPWM_CHANNEL_EDGE_MODE
  channelsetup[0].channelPolarity = MCPWM_CHANNEL_PASSIVE_LO
  channelsetup[0].channelDeadtimeEnable = FunctionalState.DISABLE
  channelsetup[0].channelDeadtimeValue = 0
  channelsetup[0].channelUpdateEnable = FunctionalState.ENABLE
  channelsetup[0].channelTimercounterValue = 0
  channelsetup[0].channelPeriodValue = 900
  channelsetup[0].channelPulsewidthValue = 450

  channelsetup[1].channelType = MCPWM_CHANNEL_EDGE_MODE
  channelsetup[1].channelPolarity = MCPWM_CHANNEL_PASSIVE_LO
  channelsetup[1].channelDeadtimeEnable = FunctionalState.DISABLE
  channelsetup[1].channelDeadtimeValue = 0
  channelsetup[1].channelUpdateEnable = FunctionalState.ENABLE
  channelsetup[1].channelTimercounterValue = 0
  channelsetup[1].channelPeriodValue = 900
  channelsetup[1].channelPulsewidthValue = 200

  channelsetup[2].channelType = MCPWM_CHANNEL_EDGE_MODE
  channelsetup[2].channelPolarity = MCPWM_CHANNEL_PASSIVE_LO
  channelsetup[2].channelDeadtimeEnable = FunctionalState.DISABLE
  channelsetup[2].channelDeadtimeValue = 0
  channelsetup[2].channelUpdateEnable = FunctionalState.ENABLE
  channelsetup[2].channelTimercounterValue = 0
  channelsetup[2].channelPeriodValue = 900
  channelsetup[2].channelPulsewidthValue = 200

  MCPWM_ConfigChannel(LPC_MCPWM, 0, channelsetup[0].ptr)
  MCPWM_ConfigChannel(LPC_MCPWM, 1, channelsetup[1].ptr)
  MCPWM_ConfigChannel(LPC_MCPWM, 2, channelsetup[2].ptr)

  #DC Mode
  MCPWM_DCMode(LPC_MCPWM, FunctionalState.ENABLE, FunctionalState.DISABLE, (0))

  MCPWM_Start(LPC_MCPWM, FunctionalState.ENABLE, FunctionalState.ENABLE, FunctionalState.ENABLE)

  try:
    while True:
      #MCPWM_WriteToShadow(LPC_MCPWM, 0, channelsetup[0].ptr) #Change the speed
      for i in range(6):
        BLDC_commutate(i)
  except:
    MCPWM_Stop(LPC_MCPWM, FunctionalState.ENABLE, FunctionalState.ENABLE, FunctionalState.ENABLE)
    heartbeatOn()
    print "you broke it"
