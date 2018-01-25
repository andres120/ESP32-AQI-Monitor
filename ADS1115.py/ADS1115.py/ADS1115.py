
# Based on https://cdn-shop.adafruit.com/datasheets/ads1115.pdf
# xx depends on the address pin connection
# 00 ground (Default, disconnected)
# 01 vdd
# 10 sda
# 11 scl

# GPIO Library
# https://makezine.com/projects/tutorial-raspberry-pi-gpio-pins-and-python/
# https://sourceforge.net/p/raspberry-gpio-python/wiki/Inputs/

import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

SDA = 18
SCL = 19

GPIO.setup(SCL, GPIO.OUT)
GPIO.setup(SDA, GPIO.OUT)

from time import sleep

ID = '10010000'
CONF_REG = '00000001'
CONFIGH = '10000001'
CONFIGL = '00100011'
WRITE = '00000001'
READ = '10010000'
CONV_REG = '00000000'
CONV_CH = '00000000'

# CLK Delay
f = 0.000001
def clk():
 sleep(f)
 GPIO.output(SCL, 1)
 sleep(f)
 GPIO.output(SCL, 0)
 sleep(f)

def to_bits(h):
 return (bin(h)[2:]).zfill(8)

def start():
 GPIO.setup(SDA, GPIO.OUT)
 GPIO.output(SDA, 0)
 sleep(f)
 GPIO.output(SCL, 0)
 sleep(f)

def stop():
 GPIO.setup(SDA, GPIO.OUT)
 GPIO.output(SDA, 1)
 sleep(f)
 GPIO.output(SCL, 1)
 sleep(f)

def send_byte(byte):
 GPIO.setup(SDA, GPIO.OUT)
 for bit in byte:
  GPIO.output(SDA, int(bit))
  clk()

 GPIO.setup(SDA, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

def ack_adc():
 clk()

def ack_master(a):
 print("set sda as output")
 print("sda " + str(a))
 clk()
 print("sda 0")


def read_bit():
 sleep(f)
 GPIO.output(SCL, 1)
 sleep(f)
 rb = GPIO.input(SDA)
 sleep(f)
 GPIO.output(SCL, 0)
 print(rb)
 return(rb)

def read_bytes(l=2):
 data = []
 start()
 for bt in range(l):
  GPIO.setup(SDA, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
  for bi in range(8):
   data.append(int(read_bit()))
   
  GPIO.setup(SDA, GPIO.OUT)
  GPIO.output(SDA, 0)
  clk()
  GPIO.output(SDA, 1)
  sleep(f)
  GPIO.output(SCL, 1)
  sleep(f)

 stop()
 return(data)

def configure_adc():
 start()
 send_byte(ID)
 ack_adc()
 send_byte('00000001')
 ack_adc()
 send_byte('11000001')
 ack_adc()
 send_byte('10000011')
 ack_adc()
 stop()

def read_adc():
 data = []
 start()
 send_byte(ID)
 ack_adc()
 send_byte('00000000')
 ack_adc()
 stop()
 sleep(f)
 start()
 send_byte('10010001')
 ack_adc()
 read_bytes()
 ack_adc()
 stop()
 return data
