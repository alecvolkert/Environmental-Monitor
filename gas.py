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
class GAS:
    def __init__(self, i2c_dev):
        self.bus = i2c_dev
        

    def contact(self, channel):
        
        config = [
            0x40 | (channel << 4),
            0x83
        ]
	bus.write_i2c_block_data(address, 0x01 ,config)
	while true:
		result = bus.read_i2c_block_data(address, 0x01 ,2)
		if result[0] & 0x80:
			break

        data = bus.read_i2c_block_data(address, 0x00, 2)

        return (data[0] << 4 | data[1] >> 4)

    def to_volts(self, raw):
        voltage = raw * (4.096/2048)
        return voltage

    def to_value(self, voltage):
        if voltage == 0:
            return float('inf')
        sensor_read = resistance_ref * (3.3 - voltage)/voltage
        return sensor_read

    def get_all(self):
        readings = {}
        for name, channel in channels.items():
            raw = self.contact(channel)
            voltage = self.to_volts(raw)
            value = self.to_value(voltage)
            readings[name] = value
        return readings
        
    def get_desired(self, name):
        reading = {}
        raw = self.contact(channels[name])
        voltage = self.to_volts(raw)
        value = self.to_value(voltage)
        reading[name] = value
        return reading
