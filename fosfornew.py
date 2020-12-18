import os     #importing os library so as to communicate with the system
import sys
import time   #importing time library to make Rpi wait because its too impatient 
os.system ("sudo pigpiod") #Launching GPIO library
time.sleep(1) # As i said it is too impatient and so if this delay is removed you will get an error
import pigpio #importing GPIO library
import RPi.GPIO as GPIO
import pygame
import dht11
GPIO.setwarnings(False)

#BOS PINLER
#19
ESC0 = 9 #Connect the ESC1 in this GPIO pin 
ESC1 = 4
ESC2 = 14
ESC3 = 27
ESC4 = 20

ROLE0 = 17 #updown
ROLE1= 10 #updown
ROLE2 = 15 #leftright
ROLE3 = 22 #leftright
ROLE4 = 21
ROLEGUC = 18
#ultrasonik1:TX:18:RX:23
#ultrasonik2:TX:25:RX:24
#
A0=0
A1=0
A2=0
A3=0
A4=0
A5=0


pygame.init()
pygame.joystick.init()

GPIO.setmode(GPIO.BCM)
GPIO.setup(ESC0, GPIO.OUT)
GPIO.setup(ESC1, GPIO.OUT)
GPIO.setup(ESC2, GPIO.OUT)
GPIO.setup(ESC3, GPIO.OUT)
GPIO.setup(ESC4, GPIO.OUT)

GPIO.setup(ROLE0, GPIO.OUT)
GPIO.setup(ROLE1, GPIO.OUT)
GPIO.setup(ROLE2, GPIO.OUT)
GPIO.setup(ROLE3, GPIO.OUT)
GPIO.setup(ROLE4, GPIO.OUT)
GPIO.setup(ROLEGUC, GPIO.OUT)


GPIO.output(ROLE0, A0)
GPIO.output(ROLE1, A1)
GPIO.output(ROLE2, A2)
GPIO.output(ROLE3, A3)
GPIO.output(ROLE4, A4)
GPIO.output(ROLEGUC, A5)

try:
    j = pygame.joystick.Joystick(0) # create a joystick instance
    j.init() # init instance
    print ("Enabled joystick: {0}".format(j.get_name()))
except pygame.error:
    print ("no joystick found.")
    sys.exit()

pi = pigpio.pi();
pi.set_servo_pulsewidth(ESC0, 0)  #RPM 0
pi.set_servo_pulsewidth(ESC1,0) #RPM 0
pi.set_servo_pulsewidth(ESC2, 0)  #RPM 0
pi.set_servo_pulsewidth(ESC3,0) #RPM 0
pi.set_servo_pulsewidth(ESC4, 0)  #RPM 0
max_value = 2000
min_value = 700
def calibrate():
    pi.set_servo_pulsewidth(ESC0, 0)  #RPM 0
    pi.set_servo_pulsewidth(ESC1,0) #RPM 0
    pi.set_servo_pulsewidth(ESC2, 0)  #RPM 0
    pi.set_servo_pulsewidth(ESC3,0) #RPM 0
    pi.set_servo_pulsewidth(ESC4, 0)  #RPM 0
    print("Disconnect the battery and press Enter")
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.JOYBUTTONDOWN:
                if event.button == 9:
                    pi.set_servo_pulsewidth(ESC0, max_value)
                    pi.set_servo_pulsewidth(ESC1, max_value)
                    pi.set_servo_pulsewidth(ESC2, max_value)
                    pi.set_servo_pulsewidth(ESC3, max_value)
                    pi.set_servo_pulsewidth(ESC4, max_value)
                    print("Prizi tak")
                    time.sleep(3)
                    GPIO.output(ROLEGUC,1)
                    time.sleep(2)
                    if event.button == 9:
                        pi.set_servo_pulsewidth(ESC0, min_value)
                        pi.set_servo_pulsewidth(ESC1, min_value)
                        pi.set_servo_pulsewidth(ESC2, min_value)
                        pi.set_servo_pulsewidth(ESC3, min_value)
                        pi.set_servo_pulsewidth(ESC4, min_value)
                       
                        time.sleep(4)
                        print "BEKLE ...."
                        time.sleep (3)
                       
                        pi.set_servo_pulsewidth(ESC0, 0)
                        pi.set_servo_pulsewidth(ESC1, 0)
                        pi.set_servo_pulsewidth(ESC2, 0)
                        pi.set_servo_pulsewidth(ESC3, 0)
                        pi.set_servo_pulsewidth(ESC4, 0)
                        time.sleep(2)
                        print "ESC ACIYORUM HAZIR MIYIZ..."
                        pi.set_servo_pulsewidth(ESC0, min_value)
                        pi.set_servo_pulsewidth(ESC1, min_value)
                        pi.set_servo_pulsewidth(ESC2, min_value)
                        pi.set_servo_pulsewidth(ESC3, min_value)
                        pi.set_servo_pulsewidth(ESC4, min_value)
                        time.sleep(1)
                        print "DEVAM"
                        control()
def control():
    print("LETS GOO. ")
    time.sleep(1)
    speed =1000
    instance = dht11.DHT11(pin=25)
    durak = True
    while durak:
        # pi.set_servo_pulsewidth(ESC0, speed)
        # pi.set_servo_pulsewidth(ESC1, speed)
        result = instance.read()
        if result.is_valid():
            print(result.temperature)
            print(result.humidity)
            if(result.humidity >= 80):
                GPIO.output(ROLEGUC,0)
            #else:
             #   GPIO.output(ROLEGUC,1)
                
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print('KAPAT ')
                sys.exit()
            if event.type == pygame.JOYHATMOTION:
                if event.value[0] == 1:
                    print("SAG")
                    GPIO.output(ROLE0, 1)
                    GPIO.output(ROLE1, 0)
                if event.value[0] == -1:
                    print("SOL")
                    GPIO.output(ROLE0, 0)
                    GPIO.output(ROLE1, 1)
                if event.value[1] == 1:
                    print("ILERI")
                    GPIO.output(ROLE0, 0)
                    GPIO.output(ROLE1, 0)
                if event.value[1] == -1:
                    print("GERI")
                    GPIO.output(ROLE0, 1)
                    GPIO.output(ROLE1, 1)
            if event.type == pygame.JOYBUTTONDOWN:
                if event.button == 5:#R1
                    pi.set_servo_pulsewidth(ESC0, speed)
                    pi.set_servo_pulsewidth(ESC1, speed)
                if event.button == 4:#L1
                    pi.set_servo_pulsewidth(ESC2, speed)
                    pi.set_servo_pulsewidth(ESC3, speed)
                    pi.set_servo_pulsewidth(ESC4, speed)
                if event.button == 1:#O
                    pi.set_servo_pulsewidth(ESC2, 1100)
                    pi.set_servo_pulsewidth(ESC3, 1100)
                    pi.set_servo_pulsewidth(ESC4, 1100)
                if event.button == 3:#kare
                    pi.set_servo_pulsewidth(ESC2, 0)
                    pi.set_servo_pulsewidth(ESC3, 0)
                    pi.set_servo_pulsewidth(ESC4, 0)
                if event.button == 6:#L2
                    print ("l2 has been pressed")
                    speed -= 100
                    print(speed)
		    if speed<=500:
			speed=500
                if event.button == 7:#R2
                    print ("r2 has been pressed")
                    speed += 100
                    print(speed) # Up
		    if speed >=2000:
			speed =2000
                if event.button == 8:
                    durak = False
                    print("BYE BITCH")
                    sys.exit()
                    #os.system("sudo python2 \home\pi\start.py")
            if event.type == pygame.JOYBUTTONUP:
                if event.button == 5:#R1
                    pi.set_servo_pulsewidth(ESC0, 0)
                    pi.set_servo_pulsewidth(ESC1, 0)
                if event.button == 4:#L1
                    pi.set_servo_pulsewidth(ESC2, 0)
                    pi.set_servo_pulsewidth(ESC3, 0)
                    pi.set_servo_pulsewidth(ESC4, 0)
                
            if event.type == pygame.JOYAXISMOTION:  # Joystick
                # if j.get_axis(0) >= 0.2:
                #     print ("right has been pressed")  # Right
                #     print(j.get_axis(0))
                # if j.get_axis(0) <= -0.2:
                #     print ("left has been pressed")   # Left
                #     print(j.get_axis(0))
                if j.get_axis(1) >= 0.8:
                    GPIO.output(ROLE2, 0)
                    GPIO.output(ROLE3, 0)
                    GPIO.output(ROLE4, 0)
                    
                    print("ASAGI")
                if j.get_axis(1) <= -0.8:
                    GPIO.output(ROLE2, 1)
                    GPIO.output(ROLE3, 1)
                    GPIO.output(ROLE4, 1)
                    print("YUKARI")
                # if j.get_axis(3) >= 0.2:
                #     print ("down has been pressed")  # Right
                #     print(j.get_axis(3))
                # if j.get_axis(3) <= -0.2:
                #     print ("up has been pressed")   # Left
                #     print(j.get_axis(3))
                # if j.get_axis(4) >= 0.2:
                #     print(j.get_axis(4)) # Down
                # if j.get_axis(4) <= -0.2:
                #     print(j.get_axis(4))   # Up
                # if j.get_axis(2) <= -0.8: #r2
                #     print ("r2 has been pressed")
                #     speed += 10
                #     print(speed) # Down
                # if j.get_axis(2) >= 0.8: #L2
                #     print ("l2 has been pressed")
                #     speed -= 10
                #     print(speed) # Up
calibrate()
            
