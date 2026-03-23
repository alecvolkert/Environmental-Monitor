import psycopg2
from dotenv import load_dotenv
import os
import requests

load_dotenv()

conn = psycopg2.connect(
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USERNAME"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT")
    )

def add_to_database(readings):
    cur = conn.cursor()
    keys = list(readings.keys())
    values = list(readings.values())

    columns = ", ".join(keys)
    placeholders = ", ".join(["%s"] * len(values))
    cur.execute("INSERT INTO enviroreadings ({columns}) VALUES ({placeholders})", values)
    conn.commit()
    send(readings)

def send(dict):
    headers = {"API_KEY": os.get_env("API_KEY")}
    requests.post(
    "https://alecvolkertenvironment.com/api/submit",
    json=dict,
    headers=headers
    )
