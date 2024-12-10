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
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/passengers"
    )

    # Query all precipitation
    results = session.query(measurement.date, measurement.prcp).all()

@app.route("/api/v1.0/names")
    # Create a dictionary from the row data and append to a list of all_passengers
    all_precipitation = []
    for date, prcp in results:
        prpc_dict = {}
        prpc_dict["date"] = date
        prpc_dict["prpc"] = precipitation
        all_precipitation.append(prpc_dict)

    return jsonify(all_passengers)


if __name__ == '__main__':
    app.run(debug=True)


#################################################
# Flask Routes
#################################################