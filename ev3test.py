#!/usr/bin/env python3

from time import sleep

from ev3dev2.motor import LargeMotor, MediumMotor, OUTPUT_A, OUTPUT_B, OUTPUT_C

from ev3dev2.sensor import INPUT_1, INPUT_2,INPUT_3
from ev3dev2.sensor.lego import TouchSensor, ColorSensor

m_right = LargeMotor(OUTPUT_A)
m_left = LargeMotor(OUTPUT_B)

s_right = ColorSensor(INPUT_2)
s_left = ColorSensor(INPUT_3)
turn=1
speed = -10
last_turn = 0
m_right.off()
m_left.off()
while True:
	print('Color 1 ' + str(s_right.rgb) + ' detected as ' + str(s_right.color_name) + '.')
	print('Color 2 ' + str(s_left.rgb) + ' detected as ' + str(s_left.color_name) + '.')
	if last_turn == 0:
		if (str(s_right.color_name) == "White" and str(s_left.color_name) == "White"):
			print('forward')
			m_right.on(speed)
			m_left.on(speed)
		if (str(s_right.color_name) == "Black" and str(s_left.color_name) == "Black"):
			print('forward_crossing')
			m_right.on(speed)
			m_left.on(speed)
		if (str(s_right.color_name) == "Black" and str(s_left.color_name) == "White"):
			if turn == 1:
				print('right_turn')
				m_right.on(speed*-1)
				m_left.on(speed*-1)
				sleep(0.5)
				m_right.on(speed*-1)
				m_left.on(speed)
				sleep(0.25)
				turn = 0
			else:
				print('right_turn')
				m_right.on(speed*-1)
				m_left.on(speed*-1)
				sleep(0.5)
				m_right.on(speed*-1)
				m_left.on(speed)
				sleep(0.5)
				turn = 1
		if (str(s_right.color_name) == "White" and str(s_left.color_name) == "Black"):
			if turn == 1:
				print('left_turn')
				m_right.on(speed*-1)
				m_left.on(speed*-1)
				sleep(0.5)
				m_right.on(speed)
				m_left.on(speed*-1)
				sleep(0.25)
				turn = 0
			else:
				print('left_turn')
				m_right.on(speed*-1)
				m_left.on(speed*-1)
				sleep(0.5)
				m_right.on(speed)
				m_left.on(speed*-1)
				sleep(0.5)
				turn = 1



