# Import the dependencies.

import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

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
# Initialize the Flask app instance
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available API routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )

    # Query all precipitation
    results = session.query(measurement.date, measurement.prcp).all()

@app.route("/api/v1.0/precipitation")
    
def precipitation():
    """Return the precipitation data for the last year."""

    # Create a dictionary from the row data and append to a list of all_passengers
    all_precipitation = []
    for date, prcp in results:
        prpc_dict = {}
        prpc_dict["date"] = date
        prpc_dict["prpc"] = prpc
        all_precipitation.append(prpc_dict)

    return jsonify(all_precipitation)

@app.route("/api/v1.0/stations")
def station():
 """Return a list of stations."""

    # Query all precipitation
results = session.query(station.station).all()

    # Convert the results into a list
all_stations = []
    for station in results:
    station_dict = {}
    station_dict["station"] = station
    all_stations.append(station_dict)
# Return as JSON
return jsonify(all_stations)  

if __name__ == '__main__':
    app.run(debug=True)
