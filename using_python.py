from m5stack import *
from m5stack_ui import *
from uiflow import *
import time
import unit


screen = M5Screen()
screen.clean_screen()
screen.set_screen_bg_color(0xFFFFFF)
servo_1 = unit.get(unit.SERVO, unit.PORTC)
color_0 = unit.get(unit.COLOR, unit.PAHUB0)
ncir_1 = unit.get(unit.NCIR, unit.PAHUB1)
Watering_0 = unit.get(unit.WATERING, unit.PORTB)


color = None
high_temp = None
low_temp = None
temp = None
max2 = None
min2 = None
water = None



label0 = M5Label('label0', x=45, y=74, color=0x000, font=FONT_MONT_14, parent=None)
touch_button0 = M5Btn(text='Feed', x=177, y=143, w=70, h=30, bg_c=0xFFFFFF, text_c=0x000000, font=FONT_MONT_14, parent=None)
bar0 = M5Bar(x=179, y=77, w=100, h=12, min=0, max=100, bg_c=0xa0a0a0, color=0x08A2B0, parent=None)
label1 = M5Label('label1', x=49, y=152, color=0x000, font=FONT_MONT_14, parent=None)
label2 = M5Label('Water Level:', x=177, y=45, color=0x000, font=FONT_MONT_14, parent=None)
touch_button1 = M5Btn(text='Pump water', x=177, y=102, w=100, h=30, bg_c=0xFFFFFF, text_c=0x000000, font=FONT_MONT_14, parent=None)


# Describe this function...
def turn_on_servo():
  global color, high_temp, low_temp, temp, max2, min2, water
  for count in range(2):
    servo_1.write_us(2)
    wait(2)
    servo_1.write_us(0)
    wait(2)
    continue

# Describe this function...
def monitor_water_color():
  global color, high_temp, low_temp, temp, max2, min2, water
  color = color_0.rawData
  label0.set_text('Color')
  label0.set_text_color((color_0.red << 16) | (color_0.green << 8) | color_0.blue)

# Describe this function...
def monitor_temperature():
  global color, high_temp, low_temp, temp, max2, min2, water
  high_temp = 27
  low_temp = 23
  temp = ncir_1.temperature
  if temp >= high_temp:
    label1.set_text('Temp is high!')
  else:
    if temp < low_temp:
      label1.set_text('Temp is low!')

# Describe this function...
def pump_water():
  global color, high_temp, low_temp, temp, max2, min2, water
  Watering_0.set_pump_status(0)
  bar0.set_range(0, 100)
  max2 = 1900
  min2 = 1600
  bar0.set_range(min2, max2)
  for count2 in range(10):
    wait_ms(500)
    water = Watering_0.get_adc_value()
    label2.set_text(str(water))
    bar0.set_value((2000 - water))
    if water < min2:
      Watering_0.set_pump_status(0)
      continue
    else:
      if water >= max2:
        Watering_0.set_pump_status(1)
        continue
      continue
    continue


def touch_button0_pressed():
  global color, high_temp, low_temp, temp, max2, min2, water
  turn_on_servo()
  pass
touch_button0.pressed(touch_button0_pressed)

def touch_button1_pressed():
  global color, high_temp, low_temp, temp, max2, min2, water
  pump_water()
  pass
touch_button1.pressed(touch_button1_pressed)


while True:
  pump_water()
  monitor_water_color()
  monitor_temperature()
  wait_ms(2)
