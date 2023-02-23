import rv3028_pico
import servo_3001HB_pico
import utime
from machine import Pin
            
# Mode select (timing or button)
MODE = 'timing'

# Timing variables
HOUR_ON_L = 5
MIN_ON_L = 45
HOUR_OFF_L = 6
MIN_OFF_L = 45

HOUR_ON_S = 6
MIN_ON_S = 0
HOUR_OFF_S = 6
MIN_OFF_S = 25

LONGSHORT = False

# Button mode variables
BUTTON_STATUS = False
BUTTON_PIN = 9
button = Pin(BUTTON_PIN, Pin.IN, Pin.PULL_UP)

# LED Pin Numbers
PICO_LED_PIN = 25
BLUE_LED_PIN = 27

# Machine set-up
servo = servo_3001HB_pico.SERVO3001HB()
rv = rv3028_pico.RV3028()
picoled = Pin(PICO_LED_PIN, Pin.OUT)
blueled = Pin(BLUE_LED_PIN, Pin.OUT)

#Sanity checking the date and time
datetime = rv.read_datetime(no_weekday=True)
print(datetime)

# Initial timing variables
t0 = rv3028_pico.generate_unixtime(datetime)
button_last = utime.ticks_ms()

# Initializing heat status
heat_on = False
switch_counter = 0

# Setting button handling
def button_handler(pin):
    global BUTTON_STATUS, button_last, blueled
      
    if utime.ticks_diff(utime.ticks_ms(), button_last) > 500:
        if BUTTON_STATUS:
            BUTTON_STATUS = False
        else:
            BUTTON_STATUS = True
            blueled.value(1)
            utime.sleep(0.150)
            blueled.value(0)
        button_last = utime.ticks_ms()

button.irq(trigger = Pin.IRQ_RISING, handler = button_handler)

# Mainloop
while True:
    # Read in times
    datetime = rv.read_datetime(no_weekday=True)
    #t = rv3028_pico.generate_unixtime(datetime)

    HOUR_ON = HOUR_ON_L
    MIN_ON = MIN_ON_L
    HOUR_OFF = HOUR_OFF_L
    MIN_OFF = MIN_OFF_L

    if LONGSHORT and (MODE != 'button'):
        if datetime[3] % 2 != 0:
            HOUR_ON = HOUR_ON_S
            MIN_ON = MIN_ON_S
            HOUR_OFF = HOUR_OFF_S
            MIN_OFF = MIN_OFF_S

    # If button is triggered or in timing mode, check time for heat
    if BUTTON_STATUS or (MODE == 'timing'):
        # Check heating status and hour/minute
        if (heat_on == False):
            if (datetime[3] == HOUR_ON) and (datetime[4] == MIN_ON):
                servo.switch_on()
                heat_on = True
                switch_counter += 1
        elif (heat_on == True):
            if (datetime[3] == HOUR_OFF) and (datetime[4] == MIN_OFF):
                servo.switch_off()
                heat_on = False
                BUTTON_STATUS = False
                switch_counter += 1

    # Turn on blue LED to indicate that the switch code ran
    if switch_counter == 2:
        blueled.value(1)
    else:
        blueled.value(0)

    # Reset the blue LED at noon
    if (datetime[3] == 12) and (datetime[4] == 0):
        switch_counter = 0
   
    # Sleep and blink LED to indicate that the loop is running
    # Blink Pico LED differently if the year has reset, indicating a problem
    if datetime[0] == 0:
        picoled.value(1)
        utime.sleep_ms(150)
        picoled.value(0)
        utime.sleep_ms(150)
        picoled.value(1)
        utime.sleep_ms(150)
    elif BUTTON_STATUS == True:
        picoled.value(1)
        utime.sleep_ms(300)
        picoled.value(0)
        utime.sleep_ms(150)
        picoled.value(1)
        utime.sleep_ms(150)
    else:
        picoled.value(1)
        utime.sleep_ms(500)
    picoled.value(0)

    utime.sleep(2)
