import time
import data
import sensors


def main():
    try:
        while True:
            readings = sensors.get_readings()
            data.add_to_database(readings)
            time.sleep(120)

    except KeyboardInterrupt:
        print("Exit")
