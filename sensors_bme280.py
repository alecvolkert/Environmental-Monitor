import smbus2 
from subprocess import PIPE, Popen

bus = smbus2.SMBus(1)

BME280_ADDRESS = 0x76
TEMP_CONFIG_REGISTER = 0x88
PRESSURE_CONFIG_REGISTER = 0x8E
HUMIDITY_DIG_H1_CONFIG_ADDRESS = 0xA1
HUMIDITY_DIG_H2_CONFIG_ADDRESS = 0xE1
HUMIDITY_DIG_H3_CONFIG_ADDRESS = 0xE3
HUMIDITY_DIG_H4_CONFIG_ADDRESS = 0xE4
HUMIDITY_DIG_H6_CONFIG_ADDRESS = 0xE7
CTRL_MEAS=0xF4
CONFIG=0xF5
CTRL_HUM=0xF2
HUM_ADD=0xFD
PRESS_ADD=0xF7
TEMP_ADD=0xFA


class BME280:
        
    def __init__(self, i2c_dev):
        self.bus = i2c_dev
        self.calibration_params()
        self.set_hum(0x01)
        self.set_filter(0xA0)
        self.set_mode(0x27)


    def calibration_params(self):
        temp_config = bus.read_i2c_block_data(BME280_ADDRESS, TEMP_CONFIG_REGISTER, 6)
        self.dig_T1 = temp_config[1] << 8 | temp_config[0]
        self.dig_T2 = temp_config[3] << 8 | temp_config[2]
        if self.dig_T2 > 32767:
            self.dig_T2 -= 65536
        self.dig_T3 = temp_config[5] << 8 | temp_config[4]
        if self.dig_T3 > 32767:
            self.dig_T3 -= 65536

        pressure_config = bus.read_i2c_block_data(BME280_ADDRESS, PRESSURE_CONFIG_REGISTER, 18)
        self.dig_P1 = pressure_config[1] << 8 | pressure_config[0]
        self.dig_P2 = pressure_config[3] << 8 | pressure_config[2]
        if self.dig_P2 > 32767:
            self.dig_P2 -= 65536
        self.dig_P3 = pressure_config[5] << 8 | pressure_config[4]
        if self.dig_P3 > 32767:
            self.dig_P3 -= 65536
        self.dig_P4 = pressure_config[7] << 8 | pressure_config[6]
        if self.dig_P4 > 32767:
            self.dig_P4 -= 65536
        self.dig_P5 = pressure_config[9] << 8 | pressure_config[8]
        if self.dig_P5 > 32767:
            self.dig_P5 -= 65536
        self.dig_P6 = pressure_config[11] << 8 | pressure_config[10]
        if self.dig_P6 > 32767:
            self.dig_P6 -= 65536
        self.dig_P7 = pressure_config[13] << 8 | pressure_config[12]
        if self.dig_P7 > 32767:
            self.dig_P7 -= 65536
        self.dig_P8 = pressure_config[15] << 8 | pressure_config[14]
        if self.dig_P8 > 32767:
            self.dig_P8 -= 65536
        self.dig_P9 = pressure_config[17] << 8 | pressure_config[16]
        if self.dig_P9 > 32767:
            self.dig_P9 -= 65536

        self.dig_H1 = bus.read_i2c_block_data(BME280_ADDRESS, HUMIDITY_DIG_H1_CONFIG_ADDRESS, 1)[0]

        humidity_dig_H2 = bus.read_i2c_block_data(BME280_ADDRESS, HUMIDITY_DIG_H2_CONFIG_ADDRESS, 2)
        self.dig_H2 = humidity_dig_H2[1] << 8 | humidity_dig_H2[0]
        if self.dig_H2 > 32767:
            self.dig_H2 -= 65536

        self.dig_H3 = bus.read_i2c_block_data(BME280_ADDRESS, HUMIDITY_DIG_H3_CONFIG_ADDRESS, 1)[0]

        humidity_dig_H4_H5 = bus.read_i2c_block_data(BME280_ADDRESS, HUMIDITY_DIG_H4_CONFIG_ADDRESS, 3)
        self.dig_H4 = (humidity_dig_H4_H5[0] << 4) | (humidity_dig_H4_H5[1] & 0x0F)
        if self.dig_H4 > 2047:
            self.dig_H4 -= 4096
        self.dig_H5 = (humidity_dig_H4_H5[1] >> 4) | (humidity_dig_H4_H5[2] << 4)
        if self.dig_H5 > 2047:
            self.dig_H5 -= 4096

        self.dig_H6 = bus.read_i2c_block_data(BME280_ADDRESS, HUMIDITY_DIG_H6_CONFIG_ADDRESS, 1)[0]
        if self.dig_H6 > 127:
            self.dig_H6 -= 256

    def set_hum(self, mode):
        bus.write_i2c_block_data(BME280_ADDRESS, CTRL_HUM, [mode])

    def set_mode(self, mode):
        bus.write_i2c_block_data(BME280_ADDRESS, CTRL_MEAS, [mode])

    def set_filter(self, filter_mode):
        bus.write_i2c_block_data(BME280_ADDRESS, CONFIG, [filter_mode])

    def get_humidity(self):
        pre_shifted_hum = bus.read_i2c_block_data(BME280_ADDRESS, HUM_ADD, 2)
        raw_shifted_hum = pre_shifted_hum[0] << 8 | pre_shifted_hum[1]
        return self.raw_to_hum(raw_shifted_hum)
    
    def get_pressure(self):
        pre_shift_press = bus.read_i2c_block_data(BME280_ADDRESS, PRESS_ADD, 3)
        raw_shifted_press = pre_shift_press[0] << 12 | pre_shift_press[1] << 4 | pre_shift_press[2] >> 4
        return self.raw_to_press(raw_shifted_press)
    
    def get_cpu_temperature(self):
        process = Popen(['vcgencmd', 'measure_temp'], stdout=PIPE, stderr=PIPE)
        output, _ = process.communicate()
        return float(output.decode().replace('temp=', '').replace("'C\n", ''))

    def get_temperature(self):
        pre_shift_temp = bus.read_i2c_block_data(BME280_ADDRESS, TEMP_ADD, 3)
        raw_shifted = pre_shift_temp[0] << 12 | pre_shift_temp[1] << 4 | pre_shift_temp[2] >> 4
        raw_temp = self.raw_to_temp(raw_shifted)
        cpu_temp = self.get_cpu_temperature()
        return raw_temp - ((cpu_temp - raw_temp) / 1.5)
    
    def raw_to_temp(self, raw):
        var1 = (raw / 16384.0 - self.dig_T1 / 1024.0) * self.dig_T2
        var2 = (raw / 131072.0 - self.dig_T1 / 8192.0) ** 2 * self.dig_T3
        self.t_fine = var1 + var2
        temperature = self.t_fine / 5120.0
        return temperature
    
    def raw_to_hum(self, raw):
        self.get_temperature()
        h = self.t_fine - 76800.0
        h = (raw - (self.dig_H4 * 64.0 + self.dig_H5 / 16384.0 * h)) * \
            (self.dig_H2 / 65536.0 * (1.0 + self.dig_H6 / 67108864.0 * h * \
            (1.0 + self.dig_H3 / 67108864.0 * h)))
        h = h * (1.0 - self.dig_H1 * h / 524288.0)
        if h > 100.0:
            h = 100.0
        elif h < 0.0:
            h = 0.0
        humidity = h
        return humidity
    
    def raw_to_press(self, raw):
        self.get_temperature()
        var1 = self.t_fine / 2.0 - 64000.0
        var2 = var1 * var1 * self.dig_P6 / 32768.0
        var2 = var2 + var1 * self.dig_P5 * 2.0
        var2 = var2 / 4.0 + self.dig_P4 * 65536.0
        var1 = (self.dig_P3 * var1 * var1 / 524288.0 + self.dig_P2 * var1) / 524288.0
        var1 = (1.0 + var1 / 32768.0) * self.dig_P1
        if var1 == 0:
            pressure = 0
        else:
            pressure = 1048576.0 - raw
            pressure = (pressure - var2 / 4096.0) * 6250.0 / var1
            var1 = self.dig_P9 * pressure * pressure / 2147483648.0
            var2 = pressure * self.dig_P8 / 32768.0
            pressure = pressure + (var1 + var2 + self.dig_P7) / 16.0
        return pressure
    
    def get_altitude(self, sea_level_pressure=1013.25):
        pressure = self.get_pressure() / 100.0 
        altitude = 44330.0 * (1.0 - (pressure / sea_level_pressure) ** (1.0 / 5.255))
        return altitude


