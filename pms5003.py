import serial
ser = serial.Serial("/dev/ttyAMA0", 9600, timeout=1)



def read():
    particle = {
        "PM1" : 0,
        "PM25": 0,
        "PM10": 0
    }
    read_bytes = ser.read_until(bytes([0x42, 0x4d]))
    particle["PM1"] = (read_bytes[8] << 4) | (read_bytes[9] >> 4)
    particle["PM25"] = (read_bytes[10] << 4) | (read_bytes[11] >> 4)
    particle["PM10"] = (read_bytes[12] << 4) | (read_bytes[13] >> 4)
    return particle




