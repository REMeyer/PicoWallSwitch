import rv3028_pico
import servo_3001HB_pico
import utime
from machine import Pin

# Switch timing variables
HOUR_ON_L = 6
MIN_ON_L = 0
HOUR_OFF_L = 6
MIN_OFF_L = 45

HOUR_ON_S = 6
MIN_ON_S = 0
HOUR_OFF_S = 6
MIN_OFF_S = 20

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

# Initial unix time
t0 = rv3028_pico.generate_unixtime(datetime)

# Initializing heat status
heat_on = False
switch_counter = 0

# Mainloop
while True:
    # Read in times
    datetime = rv.read_datetime(no_weekday=True)
    #t = rv3028_pico.generate_unixtime(datetime)

    if datetime[3] % 2 == 0:
        HOUR_ON = HOUR_ON_L
        MIN_ON = MIN_ON_L
        HOUR_OFF = HOUR_OFF_L
        MIN_OFF = MIN_OFF_L
    else:
        HOUR_ON = HOUR_ON_S
        MIN_ON = MIN_ON_S
        HOUR_OFF = HOUR_OFF_S
        MIN_OFF = MIN_OFF_S

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
    if datetime[0] != 0:
        picoled.value(1)
        utime.sleep_ms(500)
    else:
        picoled.value(1)
        utime.sleep_ms(150)
        picoled.value(0)
        utime.sleep_ms(150)
        picoled.value(1)
        utime.sleep_ms(150)
    picoled.value(0)
    utime.sleep(2)
