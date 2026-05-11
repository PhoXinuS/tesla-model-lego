#!/usr/bin/env python3

from ev3dev2.motor import LargeMotor, MediumMotor, OUTPUT_A, OUTPUT_B, OUTPUT_C, SpeedRPM
from ev3dev2.sensor import INPUT_2, INPUT_3
from ev3dev2.sensor.lego import ColorSensor
from time import sleep

# myli black jako blue
# wykrywa dobrze red, yellow, blue tak sobie 

BACKGROUND_COLOR = 'White'
T_PICKUP_COLOR = 'Red'
T_DELIVER_COLOR = 'Yellow'

SPEED = -6
APPROACH_SPEED = -6
TURN_SPEED = 10

TURN_TIME = 0.5
TURN_AROUND_TIME = 4.0
AT_BLOCK_REVERSE_TIME = 2.0
LIFT_TIME = 2.0
LIFT_RPM = 20

m_right = LargeMotor(OUTPUT_A)
m_left = LargeMotor(OUTPUT_B)

s_right = ColorSensor(INPUT_2)
s_left = ColorSensor(INPUT_3)

STATE_FOLLOW = 'follow'
STATE_BRANCH_ENTER = 'branch_enter'
STATE_APPROACH = 'approach'
STATE_AT_BLOCK = 'at_block'
STATE_RETURN_TO_T = 'return_to_t'
STATE_RETURN_TO_LINE = 'return_to_line'

current_state = STATE_FOLLOW
task_type = None  # 'pickup' or 'deliver'
turn_side = None  # 'right' or 'left'

print("Line follower ended")

m_left.off()
m_right.off()
