#!/usr/bin/env python3

from ev3dev2.motor import LargeMotor, MediumMotor, OUTPUT_A, OUTPUT_B, OUTPUT_C, SpeedRPM
from ev3dev2.sensor import INPUT_2, INPUT_3
from ev3dev2.sensor.lego import ColorSensor
from time import sleep


BACKGROUND_COLOR = 'White'
T_PICKUP_COLOR = 'Yellow'
T_DELIVER_COLOR = 'Red'
LINE_COLOR = 'Black'
LINE_COLOR2 = 'Blue'
LINE_COLOR3 = 'Brown'


SPEED = -6
APPROACH_SPEED = -6
TURN_SPEED = 10

TURN_TIME = 1.7
FORWARD_BEFORE_TURN_TIME = 1.2
TURN_AROUND_TIME = 3.5
AT_BLOCK_REVERSE_TIME = 2.0
LIFT_TIME = 0.5
LIFT_RPM = 20
BACK_TO_LIFT_TIME = 3.0
FORWARD_AFTER_LIFT_TIME = 1.0
FORWARD_TO_DROP_TIME = 7.0

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
task_type = 'pickup'  # 'pickup' or 'deliver'
turn_side = None  # 'right' or 'left'

print("Line follower started")

sleep(2)

while True:
	print('Right: '+ str(s_right.color_name) +' Left: ' + str(s_left.color_name) + ' | state: ' + str(current_state))

	# 1. Main line follower logic
	if current_state == STATE_FOLLOW:
		if s_right.color_name == BACKGROUND_COLOR and s_left.color_name == BACKGROUND_COLOR:
			# Both white
			#print('forward')
			m_right.on(SPEED)
			m_left.on(SPEED)

		elif s_right.color_name == T_PICKUP_COLOR or s_left.color_name == T_PICKUP_COLOR:
			print('FOUND PICKUP ' + 'Right: '+ str(s_right.color_name) +' Left: ' + str(s_left.color_name))
			# found the pickup point
			current_state = STATE_BRANCH_ENTER
			turn_side = 'right' if s_right.color_name == T_PICKUP_COLOR else 'left'
			m_right.off()
			m_left.off()
			continue
		elif s_right.color_name == T_DELIVER_COLOR or s_left.color_name == T_DELIVER_COLOR:
			print('FOUND DELIVERY' + 'Right: '+ str(s_right.color_name) +' Left: ' + str(s_left.color_name))
			# found the delivery point
			current_state = STATE_BRANCH_ENTER
			turn_side = 'right' if s_right.color_name == T_DELIVER_COLOR else 'left'
			m_right.off()
			m_left.off()
			continue
		elif s_right.color_name != BACKGROUND_COLOR and s_left.color_name != BACKGROUND_COLOR:
			m_right.on(SPEED)
			m_left.on(SPEED)

		elif s_right.color_name != BACKGROUND_COLOR and s_left.color_name == BACKGROUND_COLOR:
			#print('right_turn')
			m_right.on(SPEED * -1)
			m_left.on(SPEED * -1)
			m_right.on(SPEED * -1)
			m_left.on(SPEED)

		elif s_right.color_name == BACKGROUND_COLOR and s_left.color_name != BACKGROUND_COLOR:
			#print('left_turn')
			m_right.on(SPEED * -1)
			m_left.on(SPEED * -1)
			m_right.on(SPEED)
			m_left.on(SPEED * -1)

	# 2. Turn into the branch
	elif current_state == STATE_BRANCH_ENTER:
		if turn_side == 'right':
			print('Turning right into a branch  ')
			m_right.on(SPEED)
			m_left.on(SPEED)
			sleep(FORWARD_BEFORE_TURN_TIME)

			m_right.on(TURN_SPEED)
			m_left.on(-TURN_SPEED)
		else:
			print('Turning right into a branch  ')
			m_right.on(SPEED)
			m_left.on(SPEED)
			sleep(FORWARD_BEFORE_TURN_TIME)

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

		if (s_right.color_name == T_PICKUP_COLOR or s_right.color_name == T_DELIVER_COLOR) and (s_left.color_name == T_PICKUP_COLOR or s_left.color_name == T_DELIVER_COLOR):
			# found the block, stop and prepare to lift
			m_right.off()
			m_left.off()
			current_state = STATE_AT_BLOCK
			continue

		if s_right.color_name == BACKGROUND_COLOR and s_left.color_name == BACKGROUND_COLOR:
			m_right.on(APPROACH_SPEED)
			m_left.on(APPROACH_SPEED)

		elif s_right.color_name != BACKGROUND_COLOR and s_left.color_name != BACKGROUND_COLOR:
			m_right.on(APPROACH_SPEED)
			m_left.on(APPROACH_SPEED)

		elif s_right.color_name != BACKGROUND_COLOR and s_left.color_name == BACKGROUND_COLOR:
			m_right.on(APPROACH_SPEED * -1)
			m_left.on(APPROACH_SPEED * -1)
			m_right.on(APPROACH_SPEED * -1)
			m_left.on(APPROACH_SPEED)

		elif s_right.color_name == BACKGROUND_COLOR and s_left.color_name != BACKGROUND_COLOR:
			m_right.on(APPROACH_SPEED * -1)
			m_left.on(APPROACH_SPEED * -1)
			m_right.on(APPROACH_SPEED)
			m_left.on(APPROACH_SPEED * -1)

	# 4. Lift
	elif current_state == STATE_AT_BLOCK:
		# go backwards
		m_right.on(-APPROACH_SPEED)
		m_left.on(-APPROACH_SPEED)
		sleep(AT_BLOCK_REVERSE_TIME)
		
		print('turn started')
		# turn around
		m_right.on(TURN_SPEED)
		m_left.on(-TURN_SPEED)
		sleep(TURN_AROUND_TIME)
		print('end turn')
		m_right.off()
		m_left.off()
		m_right.on(APPROACH_SPEED * -1)
		m_left.on(APPROACH_SPEED  * -1)
		sleep(AT_BLOCK_REVERSE_TIME * 2)
		m_right.off()
		m_left.off()

		# pickup/deliver
		if task_type == 'pickup':
			print("payload pickup")
			lift.on_for_seconds(SpeedRPM(LIFT_RPM), LIFT_TIME)
			task_type = 'deliver'
		else:
			print("payload drop")
			m_right.on(APPROACH_SPEED)
			m_left.on(APPROACH_SPEED)
			sleep(FORWARD_TO_DROP_TIME)
			lift.on_for_seconds(SpeedRPM(-LIFT_RPM), LIFT_TIME)
			m_right.on(APPROACH_SPEED)
			m_left.on(APPROACH_SPEED)
			sleep(FORWARD_TO_DROP_TIME)
			m_left.off()
			m_right.off()

		current_state = STATE_RETURN_TO_T
		continue

	# 5. Come back to the T - junction
	elif current_state == STATE_RETURN_TO_T:
		print("returning to T junction")
		m_right.on(APPROACH_SPEED)
		m_left.on(APPROACH_SPEED)
		sleep(FORWARD_AFTER_LIFT_TIME)	
		while current_state == STATE_RETURN_TO_T:
			print('Right: '+ str(s_right.color_name) +' Left: ' + str(s_left.color_name) + ' | state: ' + str(current_state))
			if (s_right.color_name == LINE_COLOR or s_right.color_name == LINE_COLOR2 or s_right.color_name == LINE_COLOR3) and (s_left.color_name == LINE_COLOR or s_left.color_name == LINE_COLOR2 or s_left.color_name == LINE_COLOR3):
				m_right.off()
				m_left.off()
				current_state = STATE_RETURN_TO_LINE
				continue
			if s_right.color_name == BACKGROUND_COLOR and s_left.color_name == BACKGROUND_COLOR:
				print("fwd")
				m_right.on(APPROACH_SPEED)
				m_left.on(APPROACH_SPEED)

			elif s_right.color_name != BACKGROUND_COLOR and s_left.color_name == BACKGROUND_COLOR:
				print("right")
				m_right.on(APPROACH_SPEED * -1)
				m_left.on(APPROACH_SPEED * -1)
				m_right.on(APPROACH_SPEED * -1)
				m_left.on(APPROACH_SPEED)
			elif s_right.color_name == BACKGROUND_COLOR and s_left.color_name != BACKGROUND_COLOR:
				print("left")
				m_right.on(APPROACH_SPEED * -1)
				m_left.on(APPROACH_SPEED * -1)
				m_right.on(APPROACH_SPEED)
				m_left.on(APPROACH_SPEED * -1)

			else:
				print("def")
				m_right.on(APPROACH_SPEED)
				m_left.on(APPROACH_SPEED)



	# 6. Come back to the main line (turn back in the opposite direction)
	elif current_state == STATE_RETURN_TO_LINE:
		m_right.on(SPEED)
		m_left.on(SPEED)
		sleep(FORWARD_BEFORE_TURN_TIME)
		if turn_side == 'right':
			# turn left to rejoin line
			m_right.on(TURN_SPEED)
			m_left.on(-TURN_SPEED)
		else:
			# turn right
			m_right.on(-TURN_SPEED)
			m_left.on(TURN_SPEED)
		sleep(TURN_TIME)
		m_right.off()
		m_left.off()
		current_state = STATE_FOLLOW
		turn_side = None
		continue