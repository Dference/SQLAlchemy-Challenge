# Import the dependencies
from flask import Flask, jsonify
from sqlalchemy import create_engine, func
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import datetime as dt
import json

#################################################
# Database Setup
#################################################

# Create an engine to connect to the database
engine = create_engine("sqlite:///hawaii.sqlite")

# Reflect an existing database into a new model
Base = automap_base()

# Reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################

# Create an instance of Flask
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

# Define a route for the home page
@app.route("/")
def welcome():
    """List all available routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation - Precipitation observations for the last year<br/>"
        f"/api/v1.0/stations - List of stations<br/>"
        f"/api/v1.0/tobs - List of temperature observations for the last year<br/>"
        f"/api/v1.0/start_date - Minimum, average, and maximum temperatures for all dates after the start date<br/>"
        f"/api/v1.0/start_date/end_date - Minimum, average, and maximum temperatures for all dates between the start and end dates<br/>")

# Define a route to retrieve the results of the precipitation query
@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return JSON results of precipitation query"""

    # Starting from the most recent data point in the database. 
    most_recent_date = dt.datetime(2017, 8, 23)

    # Calculate the date one year from the last date in data set.
    one_year_ago = (most_recent_date - timedelta(days=365)).strftime('%Y-%m-%d')
    one_year_ago

    # Perform a query to retrieve the data and precipitation scores
    precipitation_data = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= one_year_ago).\
    filter(Measurement.date <= most_recent_date).all()

   # Convert the results into a dictionary
    precipitation_dict = {}

    # Read through the precipitation data and create the dictionary
    for date, prcp in precipitation_data:
        precipitation_dict[date] = prcp

    # Convert the dictionary to JSON format
    precipitation_json = json.dumps(precipitation_dict)

    # Now you can return `precipitation_json` wherever you need it
    return jsonify(precipitation_json)

# Define a route to retrieve the list of stations
@app.route("/api/v1.0/stations")
def stations():
    """Return a JSON list of stations from the database."""
    # Query stations from the database
    results = session.query(Station.station).all()
    # Create a list of results
    station_list = list(np.ravel(results))
    # Return the list as JSON
    return jsonify(station_list)

# Define a route to retrieve the temperature observations for the last year
@app.route("/api/v1.0/tobs")
def tobs():
    """Return a JSON list of temperature observations for the last year."""
  # Starting from the most recent data point in the database. 
    most_recent_date = dt.datetime(2017, 8, 23)
    # Find the date one year ago
    one_year_ago = (most_recent_date - timedelta(days=365)).strftime('%Y-%m-%d')
    # Query temperature observations for the last year
    results = session.query(Measurement.date, Measurement.tobs).\
            filter(Measurement.date >= one_year_ago).all()
    # Convert the results to a list of dictionaries
    tobs_data = []
    for date, tobs in results:
        tobs_dict = {}
        tobs_dict["date"] = date
        tobs_dict["tobs"] = tobs
        tobs_data.append(tobs_dict)
    # Return the list as JSON
    return jsonify(tobs_data)

# Define a route to calculate the minimum, average, and maximum temperatures for a given start date
@app.route("/api/v1.0/<start>")
def calc_temps_start(start):
    """Return a JSON list of the min, avg, and max temperatures 
    for all dates after the start date."""
    # Query the min, avg, and max temperatures for all dates after the start date
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
            filter(Measurement.date >= start).all()
    # Convert the results to a list of dictionaries
    temps_data = []
    for min_temp, avg_temp, max_temp in results:
        temps_dict = {}
        temps_dict["Min Temp"] = min_temp
        temps_dict["Avg Temp"] = avg_temp
        temps_dict["Max Temp"] = max_temp
        temps_data.append(temps_dict)
    # Return the list as JSON
    return jsonify(temps_data)

# Define a route to calculate the minimum, average, and maximum temperatures for a given date range
@app.route("/api/v1.0/<start>/<end>")
def calc_temps_start_end(start, end):
    """Return a JSON list of the min, avg, and max temperatures 
    for all dates between the start and end dates."""
    # Query the min, avg, and max temperatures for all dates between the start and end dates
    results = session.query(func.min(Measurement.tempobs), func.avg(Measurement.tempobs), func.max(Measurement.tempobs)).\
            filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    # Convert the results to a list of dictionaries
    temps_data = []
    for min_temp, avg_temp, max_temp in results:
        temps_dict = {}
        temps_dict["Min Temp"] = min_temp
        temps_dict["Avg Temp"] = avg_temp
        temps_dict["Max Temp"] = max_temp
        temps_data.append(temps_dict)
    # Return the list as JSON
    return jsonify(temps_data)

if __name__ == "__main__":
    app.run(debug=True)
