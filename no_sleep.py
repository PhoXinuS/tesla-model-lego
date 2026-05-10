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
TURN_AROUND_TIME = 1.5
PICKUP_REVERSE_TIME = 0.5
LIFT_TIME = 2.0
LIFT_RPM = 200

m_right = LargeMotor(OUTPUT_A)
m_left = LargeMotor(OUTPUT_B)
lift = MediumMotor(OUTPUT_C)

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

print("Line follower started")

while True:
	right = s_right.color_name
	left = s_left.color_name
	print(f"Right: {right}, Left: {left}   state: {current_state}")
	print('Color 1 ' + str(s_right.rgb) + ' detected as ' + str(s_right.color_name) + '.')
	print('Color 2 ' + str(s_left.rgb) + ' detected as ' + str(s_left.color_name) + '.')

	# 1. Main line follower logic
	if current_state == STATE_FOLLOW:
		if right == BACKGROUND_COLOR and left == BACKGROUND_COLOR:
			# Both white
			print('forward')
			m_right.on(SPEED)
			m_left.on(SPEED)

		elif right != BACKGROUND_COLOR and left != BACKGROUND_COLOR:
			# Both detect something
			if right == T_PICKUP_COLOR or left == T_PICKUP_COLOR:
				# found the pickup point
				current_state = STATE_BRANCH_ENTER
				task_type = 'pickup'
				turn_side = 'right' if right == T_PICKUP_COLOR else 'left'
				m_right.off()
				m_left.off()
				continue

			elif right == T_DELIVER_COLOR or left == T_DELIVER_COLOR:
				# found the delivery point
				current_state = STATE_BRANCH_ENTER
				task_type = 'deliver'
				turn_side = 'right' if right == T_DELIVER_COLOR else 'left'
				m_right.off()
				m_left.off()
				continue
			else:
				# X- junction
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

	# 2. Turn into the branch
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
		m_right.off()
		m_left.off()
		current_state = STATE_APPROACH
		continue

	# 3. Approach the block
	elif current_state == STATE_APPROACH:
		block_color = T_PICKUP_COLOR if task_type == 'pickup' else T_DELIVER_COLOR

		if right == block_color and left == block_color:
			# found the block, stop and prepare to lift
			m_right.off()
			m_left.off()
			current_state = STATE_AT_BLOCK
			continue

		if right == BACKGROUND_COLOR and left == BACKGROUND_COLOR:
			m_right.on(APPROACH_SPEED)
			m_left.on(APPROACH_SPEED)

		elif right != BACKGROUND_COLOR and left != BACKGROUND_COLOR:
			m_right.on(APPROACH_SPEED)
			m_left.on(APPROACH_SPEED)

		elif right != BACKGROUND_COLOR and left == BACKGROUND_COLOR:
			m_right.on(APPROACH_SPEED * -1)
			m_left.on(APPROACH_SPEED * -1)
			m_right.on(APPROACH_SPEED * -1)
			m_left.on(APPROACH_SPEED)

		elif right == BACKGROUND_COLOR and left != BACKGROUND_COLOR:
			m_right.on(APPROACH_SPEED * -1)
			m_left.on(APPROACH_SPEED * -1)
			m_right.on(APPROACH_SPEED)
			m_left.on(APPROACH_SPEED * -1)

	# 4. Lift
	elif current_state == STATE_AT_BLOCK:
		# go backwards
		m_right.on(-APPROACH_SPEED)
		m_left.on(-APPROACH_SPEED)
		sleep(PICKUP_REVERSE_TIME)
		m_right.off()
		m_left.off()

		# pickup/deliver
		if task_type == 'pickup':
			lift.on_for_seconds(SpeedRPM(LIFT_RPM), LIFT_TIME)
		else:
			lift.on_for_seconds(SpeedRPM(-LIFT_RPM), LIFT_TIME)

		# turn around
		m_right.on(TURN_SPEED)
		m_left.on(-TURN_SPEED)
		sleep(TURN_AROUND_TIME)
		m_right.off()
		m_left.off()

		current_state = STATE_RETURN_TO_T
		continue

	# 5. Come back to the T - junction
	elif current_state == STATE_RETURN_TO_T:
		if right != BACKGROUND_COLOR and left != BACKGROUND_COLOR:
			m_right.off()
			m_left.off()
			current_state = STATE_RETURN_TO_LINE
			continue

		elif right == BACKGROUND_COLOR and left == BACKGROUND_COLOR:
			m_right.on(APPROACH_SPEED)
			m_left.on(APPROACH_SPEED)

		elif right != BACKGROUND_COLOR and left == BACKGROUND_COLOR:
			m_right.on(APPROACH_SPEED * -1)
			m_left.on(APPROACH_SPEED * -1)
			m_right.on(APPROACH_SPEED * -1)
			m_left.on(APPROACH_SPEED)

		elif right == BACKGROUND_COLOR and left != BACKGROUND_COLOR:
			m_right.on(APPROACH_SPEED * -1)
			m_left.on(APPROACH_SPEED * -1)
			m_right.on(APPROACH_SPEED)
			m_left.on(APPROACH_SPEED * -1)

	# 6. Come back to the main line (turn back in the opposite direction)
	elif current_state == STATE_RETURN_TO_LINE:
		if turn_side == 'right':
			# turn left to rejoin line
			m_right.on(-TURN_SPEED)
			m_left.on(TURN_SPEED)
		else:
			# turn right
			m_right.on(TURN_SPEED)
			m_left.on(-TURN_SPEED)
		sleep(TURN_TIME)
		m_right.off()
		m_left.off()
		current_state = STATE_FOLLOW
		turn_side = None
		continue