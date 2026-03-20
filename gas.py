from smbus2 import SMBus
import time

bus = SMBus(1)
address = 0x49
resistance_ref = 10000

channels = {
    "oxidising": 0,
    "reducing": 1,
    "nh3": 2
}

def contact(channel):
    
    config = [
        0x42 | channel >> 4,
        0x83
    ]
    bus.write_i2c_block_data(address, 0x01 ,config)
    time.sleep(0.001)

    data = bus.read_i2c_block_data(address, 0x00, 2)

    return (data[0] << 4 | data[1] >> 4)

def to_volts(raw):
    voltage = raw * (4.096/2048)
    return voltage

def to_value(voltage):
    sensor_read = resistance_ref * (3.3 - voltage)/voltage
    return sensor_read

def get_all():
    readings = {}
    for name, channel in channels.items():
        raw = contact(channel)
        voltage = to_volts(raw)
        value = to_value(voltage)
        readings[name] = value
        return readings
    
def get_desired(name):
    reading = {}
    raw = contact(channels[name])
    voltage = to_volts(raw)
    value = to_value(voltage)
    reading[name] = value
    return reading


