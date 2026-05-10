#!/usr/bin/env python3

from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_B
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

TURN_TIME = 0.5 # we must set it experimentally
TURN_AROUND_TIME = 1.5 # this as well

m_right = LargeMotor(OUTPUT_A)
m_left  = LargeMotor(OUTPUT_B)

s_right = ColorSensor(INPUT_2)
s_left  = ColorSensor(INPUT_3)

STATE_FOLLOW = 'follow'
STATE_BRANCH_ENTER = 'branch_enter'
STATE_APPROACH = 'approach'
STATE_AT_BLOCK = 'at_block'
STATE_RETURN_TO_T = 'return_to_t'
STATE_RETURN_TO_LINE = 'return_to_line'

current_state = STATE_FOLLOW
turn_side     = None

print("Line follower started")

while True:
    right = s_right.color_name
    left  = s_left.color_name
    print(f"Right: {right}, Left: {left}   state: {current_state}")

    if current_state == STATE_FOLLOW:
        if right == BACKGROUND_COLOR and left == BACKGROUND_COLOR:
            m_right.on(SPEED)
            m_left.on(SPEED)

        elif right != BACKGROUND_COLOR and left != BACKGROUND_COLOR:
            if right == T_PICKUP_COLOR or left == T_PICKUP_COLOR:
                current_state = STATE_BRANCH_ENTER
                turn_side = 'right' if right == T_PICKUP_COLOR else 'left'
                m_right.off(); m_left.off()
                continue

            elif right == T_DELIVER_COLOR or left == T_DELIVER_COLOR:
                current_state = STATE_BRANCH_ENTER
                turn_side = 'right' if right == T_DELIVER_COLOR else 'left'
                m_right.off(); m_left.off()
                continue
            else:
                m_right.on(SPEED)
                m_left.on(SPEED)

        elif right != BACKGROUND_COLOR and left == BACKGROUND_COLOR:
            m_right.on(SPEED * -1)
            m_left.on(SPEED)

        elif right == BACKGROUND_COLOR and left != BACKGROUND_COLOR:
            m_right.on(SPEED)
            m_left.on(SPEED * -1)

    elif current_state == STATE_BRANCH_ENTER:
        if turn_side == 'right':
            # turn right in place
            m_right.on(TURN_SPEED)
            m_left.on(-TURN_SPEED)
        else:
            # turn left in place
            m_right.on(-TURN_SPEED)
            m_left.on(TURN_SPEED)
        sleep(TURN_TIME)
        m_right.off(); m_left.off()
        current_state = STATE_APPROACH
        continue

    elif current_state == STATE_APPROACH:
        if right == T_PICKUP_COLOR and left == T_PICKUP_COLOR:
            m_right.off(); m_left.off()
            current_state = STATE_AT_BLOCK
            continue
        else:
            if right != BACKGROUND_COLOR and left != BACKGROUND_COLOR:
                m_right.on(APPROACH_SPEED); m_left.on(APPROACH_SPEED)
            elif right != BACKGROUND_COLOR and left == BACKGROUND_COLOR:
                m_right.on(APPROACH_SPEED * -1); m_left.on(APPROACH_SPEED)
            elif right == BACKGROUND_COLOR and left != BACKGROUND_COLOR:
                m_right.on(APPROACH_SPEED); m_left.on(APPROACH_SPEED * -1)
            else:
                m_right.on(APPROACH_SPEED); m_left.on(APPROACH_SPEED)

    elif current_state == STATE_AT_BLOCK:
        # TODO: add code to pick up the block here
        # turn around
        m_right.on(TURN_SPEED)
        m_left.on(-TURN_SPEED)
        sleep(TURN_AROUND_TIME)
        m_right.off(); m_left.off()
        current_state = STATE_RETURN_TO_T
        continue

    elif current_state == STATE_RETURN_TO_T:
        if right != BACKGROUND_COLOR and left != BACKGROUND_COLOR:
            m_right.off(); m_left.off()
            current_state = STATE_RETURN_TO_LINE
            continue
        else:
            if right != BACKGROUND_COLOR and left == BACKGROUND_COLOR:
                m_right.on(APPROACH_SPEED * -1); m_left.on(APPROACH_SPEED)
            elif right == BACKGROUND_COLOR and left != BACKGROUND_COLOR:
                m_right.on(APPROACH_SPEED); m_left.on(APPROACH_SPEED * -1)
            else:
                m_right.on(APPROACH_SPEED); m_left.on(APPROACH_SPEED)

    elif current_state == STATE_RETURN_TO_LINE:
        if turn_side == 'right':
            m_right.on(-TURN_SPEED)
            m_left.on(TURN_SPEED)
        else:
            m_right.on(TURN_SPEED)
            m_left.on(-TURN_SPEED)
        sleep(TURN_TIME)
        m_right.off(); m_left.off()
        current_state = STATE_FOLLOW
        turn_side = None
        continue