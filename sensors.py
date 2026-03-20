
from bme280 import BME280 #temp/pressure/humidity
from smbus2 import SMBus  #bus
from ltr559 import LTR559 #
import gas
import pms5003
bus = SMBus(1)
bme280 = BME280(i2cdev = bus)
pms5003 = PMS5003()
ltr550 = LTR559()

def get_readings():
    return {    
        get_bme280(),
        get_gas(),
        get_particle()
    }

def get_bme280():
    return {
        "humidity" : bme280.get_humidity(),
        "tempurature" : bme280.get_temperature(),
        "altitude" : bme280.get_altitude(),
        "pressure" : bme280.get_pressure()
    }


def get_gas():
    return gas.get_all()


def get_particle():
    return pms5003.read()

def get_light():
    return {
        
    }
    






