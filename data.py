import psycopg2

def add_to_database(readings):
    for key, value in readings.items():
        