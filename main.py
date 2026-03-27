import time
import data
import sensors


def main():
    try:
        while True:
            readings = sensors.get_readings()
            data.add_to_database(readings)
            time.sleep(600)

    except KeyboardInterrupt:
        print("Exit")

if __name__ == "__main__":
	main()
