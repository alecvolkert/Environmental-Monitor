import serial
ser = serial.Serial("/dev/ttyAMA0", 9600, timeout=1)



def read():
    particle = {
        "PM1" : 0,
        "PM25": 0,
        "PM10": 0
    }
    ser.read_until(bytes([0x42, 0x4d]))
    read_bytes = ser.read(30)
    particle["PM1"] = (read_bytes[8] << 8) | (read_bytes[9] )
    particle["PM25"] = (read_bytes[10] << 8) | (read_bytes[11])
    particle["PM10"] = (read_bytes[12] << 8) | (read_bytes[13] )
    return particle




