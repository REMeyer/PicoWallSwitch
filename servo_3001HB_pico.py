from machine import Pin, PWM
import utime

# Duty cycle min: 4%, neutral: 7.5%, max: 11%
# So min 2650, neutral 4915, max: 7200
# From testing: 8100 max, 1800 min, 4950

SERVO_3001HB_PIN = 12
FRONT = 0.75
NEUTRAL = 0.5
BACK = 0.2

class SERVO3001HB():

    def __init__(self):

        self.servo = PWM(Pin(SERVO_3001HB_PIN))
        self.servo.freq(50)
        self.servo_move(NEUTRAL)

    def servo_move(self, p):
        '''
        Takes a percentage (p) and moves the servo
        to the range represented by p.
        '''
        
        self.servo.duty_u16(int(1800. + p*(8100. - 1800.)))

    def switch_on(self):
        #Move to turn on switch
        self.servo_move(FRONT)
        utime.sleep(0.5)
        #Move back to neutral
        self.servo_move(NEUTRAL)

    def switch_off(self):
        #Move to turn off switch
        self.servo_move(BACK)
        utime.sleep(0.5)
        #Move back to neutral
        self.servo_move(NEUTRAL)

    def move_neutral(self):
        #Move to neutral
        self.servo_move(NEUTRAL)

