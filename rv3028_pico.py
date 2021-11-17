from machine import Pin, I2C
import time

RV3028_ADDR = 0x52
SDA_PIN = 18
SCL_PIN = 19

class RV3028():

    def __init__(self):
        self.i2c = I2C(1, sda = Pin(SDA_PIN), scl = Pin(SCL_PIN),
                        freq=400000)
        self.set_bsm_mode('DSM')


    ### Reading Methods ###
    def read_seconds(self):
        byte_value = self._read(0x00, 1)
        return self._decode(byte_value)

    def read_minutes(self):
        byte_value = self._read(0x01, 1)
        return self._decode(byte_value)

    def read_hours(self):
        byte_value = self._read(0x02, 1)
        return self._decode(byte_value)

    def read_time(self):
        hours = self.read_hours()
        minutes = self.read_minutes()
        seconds = self.read_seconds()
        return (hours,minutes,seconds)

    def read_weekday(self):
        byte_value = self._read(0x03, 1)
        return self._decode(byte_value)

    def read_day_of_month(self):
        byte_value = self._read(0x04, 1)
        return self._decode(byte_value)

    def read_month(self):
        byte_value = self._read(0x05, 1)
        return self._decode(byte_value)

    def read_year(self):
        '''
        Note that year only works between 2000-2099 and is represented 
        in two digit format.
        '''
        byte_value = self._read(0x06, 1)
        return self._decode(byte_value)

    def read_date(self):
        weekday = self.read_weekday()
        day_of_month = self.read_day_of_month()
        month = self.read_month()
        year = self.read_year()
        return (year, month, day_of_month, weekday)

    def read_datetime(self, no_weekday=False):
        date = self.read_date()
        time = self.read_time()
        if no_weekday:
            return date[:-1] + time
        else:
            return date + time

    def read_unix_time(self):
        u0 = self._read(0x1B, 1)
        u1 = self._read(0x1C, 1)
        u2 = self._read(0x1D, 1)
        u3 = self._read(0x1E, 1)
        return (u0,u1,u2,u3)

    ### Setting Methods ###
    def set_bsm_mode(self, mode):
        bsm_value = int.from_bytes(self._read(0x37,1),'big')

        if mode == 'OFF':
            bytes_return = (bsm_value | 0b00000000).to_bytes(1,'big')
            print("Set BSM to Off")
        elif mode == 'DSM':
            bytes_return = (bsm_value | 0b00000100).to_bytes(1,'big')
            print("Set BSM to DSM")
        elif mode == 'LSM':
            bytes_return = (bsm_value | 0b00001100).to_bytes(1,'big')
            print("Set BSM to LSM")
        else:
            print("Improper BSM mode input...")

        self._write(0x37, bytes_return)

    def set_seconds(self, value):
        byte_value = self._encode(value)
        self._write(0x00, byte_value)

    def set_minutes(self, value):
        byte_value = self._encode(value)
        self._write(0x01, byte_value)

    def set_hours(self, value):
        byte_value = self._encode(value)
        self._write(0x02, byte_value)

    def set_time(self, time):
        hours, minutes, seconds = time
        self.set_hours(hours)
        self.set_minutes(minutes)
        self.set_seconds(seconds)

    def set_weekday(self, value):
        byte_value = self._encode(value)
        self._write(0x03, byte_value)

    def set_day_of_month(self, value):
        byte_value = self._encode(value)
        self._write(0x04, byte_value)

    def set_month(self, value):
        byte_value = self._encode(value)
        self._write(0x05, byte_value)

    def set_year(self, value):
        if value >= 0 and value <= 99:
            byte_value = self._encode(value)
        elif value >= 2000 and value <= 2099:
            byte_value = self._encode(value - 2000)
        else:
            raise ValueError('Year must be either between 0-99 or 2000-2099')

        self._write(0x06, byte_value)

    def set_date(self, date):
        weekday, day_of_month, month, year = date
        self.set_weekday(weekday)
        self.set_day_of_month(day_of_month)
        self.set_month(month)
        self.set_year(year)

    def set_datetime(self, datetime):
        '''
        Takes an tuple of (year, month, day, weekday, hour, minute, second)
        '''
        year, month, day_of_month, weekday, hours, minutes, seconds = datetime
        self.set_weekday(weekday)
        self.set_day_of_month(day_of_month)
        self.set_month(month)
        self.set_year(year)
        self.set_hours(hours)
        self.set_minutes(minutes)
        self.set_seconds(seconds)

    ### Special methods ###
    def _decode(self, value):
        upper = ((int.from_bytes(value,"big") & 0xF0) >> 4) * 10
        lower = (int.from_bytes(value,"big") & 0x0F)
        return upper + lower

    def _encode(self, value):
        upper = int(value/10) << 4
        lower = value % 10
        return (upper | lower).to_bytes(1,"big")

    def _read(self, register, byte_length):
        return self.i2c.readfrom_mem(RV3028_ADDR, register, byte_length)

    def _write(self, register, value_bytes):
        self.i2c.writeto_mem(RV3028_ADDR, register, value_bytes)

def generate_unixtime(datetime):
    '''Takes in a datetime with no weekday and returns the unixtime'''
    year, month, day_of_month, hour, minute, second = datetime
    localtime = (year,month,day_of_month, hour, minute, second, 0,0)
    unixtime = time.mktime(localtime)
    return unixtime


