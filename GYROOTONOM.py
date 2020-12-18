import os     #importing os library so as to communicate with the system
import sys
import time   #importing time library to make Rpi wait because its too impatient 
os.system ("sudo pigpiod") #Launching GPIO library
time.sleep(1) # As i said it is too impatient and so if this delay is removed you will get an error
import pigpio #importing GPIO library
import RPi.GPIO as GPIO
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
TX1=18 #MESAFE1
RX1=23 #MESAFE1
#ultrasonik2:TX:25:RX:24

A0=0
A1=0
A2=0
A3=0
A4=0
A5=0

GPIO.setmode(GPIO.BCM)
GPIO.setup(ESC0, GPIO.OUT)
GPIO.setup(ESC1, GPIO.OUT)
GPIO.setup(ESC2, GPIO.OUT)
GPIO.setup(ESC3, GPIO.OUT)
GPIO.setup(ESC4, GPIO.OUT)
GPIO.setup(TX1,GPIO.OUT) #MESAFE1
GPIO.setup(RX1,GPIO.IN)  #MESAFE1

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


pi = pigpio.pi();
pi.set_servo_pulsewidth(ESC0, 0)  #RPM 0
pi.set_servo_pulsewidth(ESC1,0) #RPM 0
pi.set_servo_pulsewidth(ESC2, 0)  #RPM 0
pi.set_servo_pulsewidth(ESC3,0) #RPM 0
pi.set_servo_pulsewidth(ESC4, 0)  #RPM 0
max_value = 2000
min_value = 700
def calibrate():
    print("calibrate girdi,esc=0")
    pi.set_servo_pulsewidth(ESC0, 0)  #RPM 0
    pi.set_servo_pulsewidth(ESC1,0) #RPM 0
    pi.set_servo_pulsewidth(ESC2, 0)  #RPM 0
    pi.set_servo_pulsewidth(ESC3,0) #RPM 0
    pi.set_servo_pulsewidth(ESC4, 0)  #RPM 0
    print("simdi döngüye girip esc=max olucak")
    while True:
        
        pi.set_servo_pulsewidth(ESC0, max_value)
        pi.set_servo_pulsewidth(ESC1, max_value)
        pi.set_servo_pulsewidth(ESC2, max_value)
        pi.set_servo_pulsewidth(ESC3, max_value)
        pi.set_servo_pulsewidth(ESC4, max_value)
        print("röle tetiklenecek")
        time.sleep(3)
        GPIO.output(ROLEGUC,1)
        time.sleep(2)
        if ROLEGUC== 1:
            pi.set_servo_pulsewidth(ESC0, min_value)
            pi.set_servo_pulsewidth(ESC1, min_value)
            pi.set_servo_pulsewidth(ESC2, min_value)
            pi.set_servo_pulsewidth(ESC3, min_value)
            pi.set_servo_pulsewidth(ESC4, min_value)
            time.sleep(4)
            print ("5s BEKLE ....")
            time.sleep (3) 
            pi.set_servo_pulsewidth(ESC0, 0)
            pi.set_servo_pulsewidth(ESC1, 0)
            pi.set_servo_pulsewidth(ESC2, 0)
            pi.set_servo_pulsewidth(ESC3, 0)
            pi.set_servo_pulsewidth(ESC4, 0)
            time.sleep(2)
            print ("ESC ACIYORUM HAZIR MIYIZ...")
            pi.set_servo_pulsewidth(ESC0, min_value)
            pi.set_servo_pulsewidth(ESC1, min_value)
            pi.set_servo_pulsewidth(ESC2, min_value)
            pi.set_servo_pulsewidth(ESC3, min_value)
            pi.set_servo_pulsewidth(ESC4, min_value)
            time.sleep(1)
            
            control()
def control():

    print ("ESC acıldı.")
    time.sleep(1)

    speed =1000
    GPIO.output(ROLE0, 0) #ileri
    GPIO.output(ROLE1, 0) #ileri
    GPIO.output(ROLE2, 0) #aşağı
    GPIO.output(ROLE3, 0) #aşağı
    GPIO.output(ROLE4, 0) #aşağı

    pi.set_servo_pulsewidth(ESC0, speed)
    pi.set_servo_pulsewidth(ESC1, speed)
    pi.set_servo_pulsewidth(ESC2, speed)
    pi.set_servo_pulsewidth(ESC3, speed)
    pi.set_servo_pulsewidth(ESC4, speed)


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

###############   MESAFE     ####################   
        GPIO.output(TX1,False)
        print("Waiting for sensor to settle")
        time.sleep(0.5)
    
        GPIO.output(TX1,True)
        time.sleep(0.00001)
        GPIO.output(TX1,False)
    
        while GPIO.input(RX1)==0:
            pulse_start = time.time()
        
        while GPIO.input(RX1)==1:
            pulse_end = time.time()
        
        pulse_duration = pulse_end - pulse_start
    
        distance = pulse_duration *17150
        distance = round(distance,2)
    
        if distance > 20 and distance <400:

            
            print("mesafe sensörü calısıyor.")
            print(distance - 0.5)
            kose=0
            donme=0
            if donme ==0:
                if kose==0:
                    if distance > 50 and distance <55:
                        print(distance - 0.5)
                        GPIO.output(ROLE0,0)
                        GPIO.output(ROLE1,1)
                        GPIO.output(ROLE2, 0)
                        GPIO.output(ROLE3, 0)
                        GPIO.output(ROLE4, 0)
                        pi.set_servo_pulsewidth(ESC0, speed)
                        pi.set_servo_pulsewidth(ESC1, speed)
                        pi.set_servo_pulsewidth(ESC2, speed)
                        pi.set_servo_pulsewidth(ESC3, speed)
                        pi.set_servo_pulsewidth(ESC4, speed)
                        if distance > 55 :
                            GPIO.output(ROLE0, 0)
                            GPIO.output(ROLE1, 0)
                            kose=1
                if kose==1 :
                    if distance > 50 and distance <55:
                        print(distance - 0.5)
                        GPIO.output(ROLE0,0)
                        GPIO.output(ROLE1,1)
                        GPIO.output(ROLE2, 0)
                        GPIO.output(ROLE3, 0)
                        GPIO.output(ROLE4, 0)
                        pi.set_servo_pulsewidth(ESC0, speed)
                        pi.set_servo_pulsewidth(ESC1, speed)
                        pi.set_servo_pulsewidth(ESC2, speed)
                        pi.set_servo_pulsewidth(ESC3, speed)
                        pi.set_servo_pulsewidth(ESC4, speed)
                        if distance > 55 :
                            GPIO.output(ROLE0, 0)
                            GPIO.output(ROLE1, 0)
                            kose=2
                if kose==2 :
                    if distance > 50 and distance <55:
                        GPIO.output(ROLE0,0)
                        GPIO.output(ROLE1,1)
                        GPIO.output(ROLE2, 0)
                        GPIO.output(ROLE3, 0)
                        GPIO.output(ROLE4, 0)
                        pi.set_servo_pulsewidth(ESC0, speed)
                        pi.set_servo_pulsewidth(ESC1, speed)
                        pi.set_servo_pulsewidth(ESC2, speed)
                        pi.set_servo_pulsewidth(ESC3, speed)
                        pi.set_servo_pulsewidth(ESC4, speed)
                        if distance > 55 :
                            GPIO.output(ROLE0, 0)
                            GPIO.output(ROLE1, 0)
                            kose=3
                if kose==3 :
                    if distance > 50 and distance <55:
                        GPIO.output(ROLE0,0)
                        GPIO.output(ROLE1,1)
                        GPIO.output(ROLE2, 0)
                        GPIO.output(ROLE3, 0)
                        GPIO.output(ROLE4, 0)
                        pi.set_servo_pulsewidth(ESC0, speed)
                        pi.set_servo_pulsewidth(ESC1, speed)
                        pi.set_servo_pulsewidth(ESC2, speed)
                        pi.set_servo_pulsewidth(ESC3, speed)
                        pi.set_servo_pulsewidth(ESC4, speed)
                        if distance > 55 :
                            GPIO.output(ROLE0, 0)
                            GPIO.output(ROLE1, 0)
                            donme=1 
                                       
            if donme == 1 :
                speed1=1200
                pi.set_servo_pulsewidth(ESC0, speed)
                pi.set_servo_pulsewidth(ESC1, speed)
                pi.set_servo_pulsewidth(ESC2, speed1)
                pi.set_servo_pulsewidth(ESC3, speed1)
                pi.set_servo_pulsewidth(ESC4, speed1)
                kose=0
                if kose==0:
                    if distance > 100 and distance <105:
                        GPIO.output(ROLE0,0)
                        GPIO.output(ROLE1,1)
                        GPIO.output(ROLE2, 0)
                        GPIO.output(ROLE3, 0)
                        GPIO.output(ROLE4, 0)
                        
                        if distance > 105 :
                            GPIO.output(ROLE0, 0)
                            GPIO.output(ROLE1, 0)
                            kose=1
                if kose==1 :
                    if distance > 100 and distance < 105 :
                        GPIO.output(ROLE0,0)
                        GPIO.output(ROLE1,1)
                        GPIO.output(ROLE2, 0)
                        GPIO.output(ROLE3, 0)
                        GPIO.output(ROLE4, 0)
                     
                        if distance > 105 :
                            GPIO.output(ROLE0, 0)
                            GPIO.output(ROLE1, 0)
                            kose=2
                if kose==2 :
                    if distance > 100 and distance <105 :
                        GPIO.output(ROLE0,0)
                        GPIO.output(ROLE1,1)
                        GPIO.output(ROLE2, 0)
                        GPIO.output(ROLE3, 0)
                        GPIO.output(ROLE4, 0)
                     
                        if distance > 105 :
                            GPIO.output(ROLE0, 0)
                            GPIO.output(ROLE1, 0)
                            kose=3
                if kose==3 :
                    if distance > 100 and distance <105:
                        GPIO.output(ROLE0,0)
                        GPIO.output(ROLE1,1)
                        GPIO.output(ROLE2, 0)
                        GPIO.output(ROLE3, 0)
                        GPIO.output(ROLE4, 0)
                       
                        if distance > 105 :
                            GPIO.output(ROLE0, 0)
                            GPIO.output(ROLE1, 0)
                            donme=2
            if donme == 2 :
                speed2=1300
                pi.set_servo_pulsewidth(ESC0, speed)
                pi.set_servo_pulsewidth(ESC1, speed)
                pi.set_servo_pulsewidth(ESC2, speed2)
                pi.set_servo_pulsewidth(ESC3, speed2)
                pi.set_servo_pulsewidth(ESC4, speed2)
                kose=0
                if kose==0:
                    if distance > 150 and distance <155:
                        GPIO.output(ROLE0,0)
                        GPIO.output(ROLE1,1)
                        GPIO.output(ROLE2, 0)
                        GPIO.output(ROLE3, 0)
                        GPIO.output(ROLE4, 0)
                      
                        if distance > 155 :
                            GPIO.output(ROLE0, 0)
                            GPIO.output(ROLE1, 0)
                            kose=1
                if kose==1 :
                    if distance > 150 and distance < 155 :
                        GPIO.output(ROLE0,0)
                        GPIO.output(ROLE1,1)
                        GPIO.output(ROLE2, 0)
                        GPIO.output(ROLE3, 0)
                        GPIO.output(ROLE4, 0)
                        
                        if distance > 155 :
                            GPIO.output(ROLE0, 0)
                            GPIO.output(ROLE1, 0)
                            kose=2
                if kose==2 :
                    if distance > 150 and distance <155 :
                        GPIO.output(ROLE0,0)
                        GPIO.output(ROLE1,1)
                        GPIO.output(ROLE2, 0)
                        GPIO.output(ROLE3, 0)
                        GPIO.output(ROLE4, 0)
                       
                        if distance > 155 :
                            GPIO.output(ROLE0, 0)
                            GPIO.output(ROLE1, 0)
                            kose=3
                if kose==3 :
                    if distance > 150 and distance <155:
                        GPIO.output(ROLE0,0)
                        GPIO.output(ROLE1,1)
                        GPIO.output(ROLE2, 0)
                        GPIO.output(ROLE3, 0)
                        GPIO.output(ROLE4, 0)
                        
                        if distance > 155 :
                            GPIO.output(ROLE0, 0)
                            GPIO.output(ROLE1, 0)
        else:   
            print("mesafe sensörü çalışmıyor")                 
               

                

        

            
               
calibrate()
            
