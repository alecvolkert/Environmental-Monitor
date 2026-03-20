CREATE DATABASE environment;
\c environment;
CREATE EXTENSION postgis;
CREATE TABLE IF NOT EXISTS enviroReadings(
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMPTZ DEFAULT NOW(),
    temperature FLOAT,
    humidity FLOAT,
    pressure FLOAT,
    CO_carbon_monoxide FLOAT,
    NO2_nitrogen_dioxide FLOAT,
    C2H5OH_ethanol FLOAT,
    H2_hydrogen FLOAT,
    NH3_ammonia FLOAT,
    CH4_methane FLOAT,
    C3H8_propane FLOAT,
    C4H10_isobutane FLOAT,
    PM1.0 FLOAT,
    PM2.5 FLOAT,
    PM10.0 FLOAT
);