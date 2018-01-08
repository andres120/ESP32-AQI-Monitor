import machine, ssd1306, utime, time, network, filter
from simple import MQTTClient
from machine import UART
from simple import MQTTClient

rate = 8000000
sck_pin = machine.Pin(18, machine.Pin.OUT)
mosi_pin = machine.Pin(23, machine.Pin.IN)
spi = machine.SPI(2, baudrate=rate, mosi = mosi_pin, sck=sck_pin)
dc  = machine.Pin(22,  machine.Pin.OUT)
cs = machine.Pin(17, machine.Pin.OUT)
res = machine.Pin(21, machine.Pin.OUT)
led = machine.Pin(25, machine.Pin.OUT)
sw = machine.Pin(36, machine.Pin.IN)
#adc = machine.ADC(machine.Pin(34))

display_status = 1
ssid = 'ssid'
ap_ps = 'pk'
oled = ssd1306.SSD1306_SPI(128, 64, spi, dc, res, cs, external_vcc=False)

utime.sleep(3)
sta_if = network.WLAN(network.STA_IF)
sta_if.active(1)
sta_if.connect(ssid, ap_ps)

while not sta_if.isconnected():
 oled.fill(0)
 oled.text("OFFLINE",0,0)
 oled.text("Connecting...",0,16)
 oled.show()
 time.sleep(1)


SERVER = '192.168.31.243'
CLIENT_ID = 'Filter'
TOPIC = b'filter_status'
client = MQTTClient(CLIENT_ID, SERVER)

def sub_cb(topic, msg):
 global speed
 global pm25
 global tm
 print(topic + "," + msg)
 if str(topic).find("speed") > -1:
  speed = int(str(msg)[1:][1:-1])
 elif str(topic).find("time") > -1:
  tm = str(msg)[1:][1:-1]
 else:
  print(msg)
  pm25 = round(float(str(msg)[1:][1:-1]),1)
client.set_callback(sub_cb)

oled.fill(0)
while True:
 led.value(1)
 for dsec in range(300):
  if not sw.value():
   print("Pressed")
   display_status = not display_status
   if display_status == 1:
    oled.poweron()
   else:
    oled.poweroff()
   time.sleep(1)
  else:
   time.sleep(0.1)
 led.value(0)
 if not sta_if.isconnected():
  oled.poweron()
  oled.fill(0)
  oled.text("Offline!",0,0)
  oled.text("Connecing...",0,16)
  oled.show()
  try:
   sta_if.connect(ssid, ap_ps)
  except:
   oled.fill(0)
   oled.text("WiFi Error!",0,32)
   global errrr
   errrr  = e
   y = 8
   for w in str(errrr).split():
    oled.text(w,0,y)
    y += 8
   oled.show()
  client.connect()
  client.publish(b'filter_error', str(errrr))
  client.disconnect()
 else:
  try:
   if display_status:
    oled.text("Waiting...",0,0)
    oled.show()
   client.connect()
   client.subscribe('pm25')
   client.subscribe('speed')
   client.subscribe('time')
   client.wait_msg()
   time.sleep(1)
   client.check_msg()
   time.sleep(1)
   client.check_msg()
   if display_status:
    oled.fill(0)
    oled.text("           Done!",0,0)
    oled.text("PM2.5: "+str(pm25),0,16)
    oled.text("Filter speed:"+str(filter.get_status()),0,32)
    oled.text(tm,0,48)
    oled.show()
   filter.set_status(speed)
   client.disconnect()
  except BaseException as e:
   global errrr
   errrr  = e
   oled.poweron()
   oled.fill(0)
   oled.text("ERROR!!!",0,0)
   y = 8
   for w in str(errrr).split():
    oled.text(w,0,y)
    y += 8
    oled.show()
   sta_if.active(0)
   time.sleep(10)
   sta_if.active(1)
   sta_if.connect(ssid, ap_ps)
   while not sta_if.isconnected():
    oled.text("Connecting...",0,56)
    oled.show()
    time.sleep(1)
    
   client.connect()
   client.publish(b'filter_error', str(errrr))
   client.disconnect()
