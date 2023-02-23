'''
Module to facilitate testing of the servo and rv3028 
through repl in rshell. Do not try running these functions
on the board alone.
'''

import rv3028_pico
import servo_3001HB_pico
import utime

class Tester:
    '''
    Class to contain testing methods for the py pico servo switch flipper.
    '''

    def __init__(self):
        # Attempt to connect to the servo and RV3028 controllers. 
        try:
            self.servo = servo_3001HB_pico.SERVO3001HB()
        except:
            print("Can not initiate servo controller")
        try:
            self.rv = rv3028_pico.RV3028()
        except:
            print("Can not initiate rv3028 controller.")


        print("Current datetime: ", self.rv.read_datetime())
        try:
            self.rv.autoset_datetime()
            print("New datetime set: ", self.rv.read_datetime())
        except:
            print("Could not automatically set time")

    def test_servo(self):
        self.servo.switch_on()
        utime.sleep(5)
        self.servo.switch_off()
        utime.sleep(1)

    def continuous_servo(self):
        #t0 = rv3028_pico.generate_unixtime(rv)
        t0 = utime.time()
        

        heat_on = False
        while True:
            t = utime.time()
            #t = rv3028_pico.generate_unixtime(rv)
            deltat = t - t0

            if deltat > 7:
                t0 = t
                if heat_on == False:
                    self.servo.switch_on()
                    heat_on = True
                elif heat_on == True:
                    self.servo.switch_off()
                    heat_on = False

            utime.sleep(1)

tester = Tester()