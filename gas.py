from smbus2 import SMBus
import time

bus = SMBus(1)
address = 0x49


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

def to_value():
    
