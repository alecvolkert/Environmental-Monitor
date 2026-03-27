
from sensors_bme280 import BME280 #temp/pressure/humidity
from smbus2 import SMBus  #bus
from gas import GAS
import sensors_pms5003
bus = SMBus(1)
bme280 = BME280(i2c_dev = bus)
gas = GAS(i2c_dev = bus)

def get_readings():
    return {    
        **get_bme280(),
        **get_gas(),
        **get_particle()
    }

def get_bme280():
    return {
        "humidity" : bme280.get_humidity(),
        "temperature" : bme280.get_temperature(),
        "altitude" : bme280.get_altitude(),
        "pressure" : bme280.get_pressure()
    }

def get_gas():
    return gas.get_all()


def get_particle():
    return sensors_pms5003.read()







