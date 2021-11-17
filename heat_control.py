import rv3028_pico
import servo_3001HB_pico
import utime

HOUR_ON = 6
MIN_ON = 0
HOUR_OFF = 6
MIN_OFF = 45

LED_PIN = 25

# Machine set-up
servo = servo_3001HB_pico.SERVO3001HB()
rv = rv3028_pico.RV3028()
led = PIN(LED_PIN, Pin.OUT)

#Sanity checking the date and time
datetime = rv.read_datetime(no_weekday=True)
print(datetime)

# Initial unix time
t0 = rv3028_pico.generate_unixtime(datetime)

# Initializing heat status
heat_on = False

# Mainloop
while True:
    # Read in times
    datetime = rv.read_datetime(no_weekday=True)
    t = rv3028_pico.generate_unixtime(datetime)

    # Check heating status and hour/minute
    if (heat_on == False):
        if (datetime[3] == HOUR_ON) and (datetime[4] == MIN_ON):
            servo.switch_on()
            heat_on = True
    elif (heat_on == True):
        if (datetime[3] == HOUR_OFF) and (datetime[4] == MIN_OFF):
            servo.switch_off()
            heat_on = False
   
    #Sleep and blink LED to indicate that the loop is running
    led.value(1)
    utime.sleep_ms(500)
    led.value(0)
    utime.sleep(14.5)
