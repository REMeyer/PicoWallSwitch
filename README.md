# Pico Wall Switch

Micropython software that provides control of a 3001HB Servo and a Pimoroni RV3028 RTC breakout board via a Raspberry Pi Pico microcontroller.

The module contains three scripts:

* rv3028_pico.py
	* Provides functionality for the RV3028 RTC breakout module
* servo_3001HB_pico.py
	* Provides very basic functionality for the 3001HB Servo
* heat_control.py
	* Mainloop script for controlling the wall switch - specialized application

This library has no specific dependancies other than micropython-included modules.
