#!/usr/bin/env python3

from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_B
from ev3dev2.sensor import INPUT_2, INPUT_3
from ev3dev2.sensor.lego import ColorSensor

SPEED = -6
BACKGROUND_COLOR = 'White'
LINE_COLOR = 'Black'

m_right = LargeMotor(OUTPUT_A)
m_left  = LargeMotor(OUTPUT_B)

s_right = ColorSensor(INPUT_2)
s_left  = ColorSensor(INPUT_3)

print("Line follower started")

while True:
    right = s_right.color_name
    left  = s_left.color_name
    print(f"Right: {right}, Left: {left}")

    if right == BACKGROUND_COLOR and left == BACKGROUND_COLOR:
        print('forward')
        m_right.on(SPEED)
        m_left.on(SPEED)

    elif right != BACKGROUND_COLOR and left != BACKGROUND_COLOR:
        print('forward_crossing')
        m_right.on(SPEED)
        m_left.on(SPEED)

    elif right != BACKGROUND_COLOR and left == BACKGROUND_COLOR:
        print('right_turn')
        m_right.on(SPEED * -1)
        m_left.on(SPEED * -1)
        m_right.on(SPEED * -1)
        m_left.on(SPEED)

    elif right == BACKGROUND_COLOR and left != BACKGROUND_COLOR:
        print('left_turn')
        m_right.on(SPEED * -1)
        m_left.on(SPEED * -1)
        m_right.on(SPEED)
        m_left.on(SPEED * -1)