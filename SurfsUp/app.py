# Import the dependencies.

import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from sqlalchemy.sql import text
from dateutil.relativedelta import relativedelta
import pandas as pd
from collections import OrderedDict

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model

Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
station = Base.classes.station
measurement = Base.classes.measurement

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

def get_one_year_prior_dt():
    # Find the most recent date in the data set.
    most_recent_date_row = session.query(measurement.date).order_by(measurement.date.desc()).first()

    # Extract the date from the row (tuple)
    most_recent_date = most_recent_date_row[0]  # This gets the first element of the tuple

    # Ensure that most_recent_date is a date object
    most_recent_date_dt = pd.to_datetime(most_recent_date)

    # Calculate the date one year from the last date in data set.
    one_year_prior = most_recent_date_dt - relativedelta(months=12)

    # Convert one_year_prior to a standard date object
    one_year_prior_dt = one_year_prior.date()  # Convert to Python datetime

    return one_year_prior_dt

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )
#################################################
# Flask Routes
#################################################
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Query all precipitation

    one_year_prior_dt = get_one_year_prior_dt()
    precipitation_results = session.query(measurement.date, measurement.prcp).filter(measurement.date >= one_year_prior_dt).order_by(measurement.date).all()

    # Create a dictionary from the row data and append to a list of all_precipitation
    all_precipitation = []
    for date, prcp in precipitation_results:
        prpc_dict = {}
        prpc_dict["date"] = date
        prpc_dict["prcp"] = prcp
        all_precipitation.append(prpc_dict)
    return jsonify(all_precipitation)

@app.route("/api/v1.0/stations")
def stations():

# List the stations and their counts in descending order.
    # active_stations = session.query(measurement.station, func.count(measurement.station)).\
    #     group_by(measurement.station).\
    #     order_by(func.count(measurement.station).desc()).all()

    active_stations = session.execute(text("SELECT m.station, s.name, COUNT(m.station) FROM measurement AS m JOIN station AS s ON s.station = m.station GROUP BY m.station ORDER BY COUNT(m.station) DESC")).fetchall()
# Query all stations into a list
    all_stations = []
    for active_station, station_name, count  in active_stations:
        station_dict = OrderedDict()
        station_dict["station"] = active_station
        station_dict["name"] = station_name
        station_dict["count"] = count
        all_stations.append(station_dict)
# Return a JSON list of stations from the dataset.
    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def temperature():
   
    one_year_prior_dt = get_one_year_prior_dt()

   # Look for the most active station id from the previous query
    most_active_station = session.query(measurement.station, func.count(measurement.station)).\
        group_by(measurement.station).\
        order_by(func.count(measurement.station).desc()).first()
    print(most_active_station[0])

    # Query the dates and temperature observations of the most-active station for the previous year of data.
    result_most_active_station = session.query(measurement.date, measurement.tobs).filter(measurement.date >= one_year_prior_dt).filter(measurement.station == most_active_station[0]).order_by(measurement.date).all()
    
    # Collect temperature observations in a list
    all_temperature = []
    for date, tobs in result_most_active_station:
            temperature_dict = {}
            temperature_dict["date"] = date
            temperature_dict["tobs"] = tobs
            all_temperature.append(temperature_dict)
    
    # Return a JSON list of temperature observations for the previous year.
    return jsonify(all_temperature)

@app.route("/api/v1.0/<start>")
def start_date(start):
    # Convert the start date from string to datetime
    start_date = pd.to_datetime(start).date()

    # Query data starting from a given start date
    start_results = session.query(
        measurement.date, 
        func.min(measurement.tobs), 
        func.avg(measurement.tobs), 
        func.max(measurement.tobs)).\
        filter(measurement.date >= start_date).all()
    
    # Create a dictionary from the row data and append to the list
    start_dict = {
        "Start Date": start_date,
        "TMIN": start_results[0][1],
        "TAVG": start_results[0][2],
        "TMAX": start_results[0][3]
    }
    # Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start date.
    return jsonify(start_dict)

@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):
   
# Convert the start date and end date from string to datetime
    start_date = pd.to_datetime(start).date()
    end_date = pd.to_datetime(end).date()

   # Query data from a given start date to an end date
    start_end_results = session.query(measurement.date, func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
        filter(measurement.date >= start_date).\
        filter(measurement.date <= end_date).all()

    start_end_dict = {
        "Start Date": start_date,
        "End Date": end_date,
        "TMIN": start_end_results[0][1],
        "TAVG": start_end_results[0][2],
        "TMAX": start_end_results[0][3]
    }
    # Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start-end range.
    return jsonify(start_end_dict)
  
if __name__ == '__main__':
    app.run(debug=True)
