import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


# Database Setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

#save references
Measurement=Base.classes.measurement
Station=Base.classes.station

#create session
session=Session(engine)

#flask setup
app = Flask(__name__)

#flask routes
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation"
        f"/api/v1.0/stations"
        f"/api/v1.0/tobs"
        f"/api/v1.0/<start>"
        f"/api/v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def perceipatation():
    session=Session(engine)
    results = session.query(
        (Measurement.date, Measurement.prcp)
        .filter(Measurement.date >= "2016-08-24")
        .all()
    )
    session.close()

    percipitation = []
    for date, prcp in results:
        percipitation_dict = {}
        percipitation_dict["date"] = date
        percipitation_dict["percipitation"] = prcp
        percipitation.append(percipitation_dict)
    
    return jsonify(percipitation)


@app.route("/api/v1.0/stations")
def stations():
    session=Session(engine)
    results = session.query(Station.name).all()

    session.close()

    stations = list(np.ravel(results))

    return jsonify(stations)


@app.route("/api/v1.0/tobs")
def tobs():
    session-Session(engine)
    results = session.query(
        (Measurement.date,  Measurement.tobs,Measurement.prcp)
        .filter(Measurement.date >= '2016-08-23')
        .filter(Measurement.station=='USC00519281')
        .order_by(Measurement.date)
        .all()
    )
    session.close()

    all_tobs = []
    for prcp, date,tobs in results:
        tobs_dict = {}
        tobs_dict["prcp"] = prcp
        tobs_dict["date"] = date
        tobs_dict["tobs"] = tobs
        
        all_tobs.append(tobs_dict)

    return jsonify(all_tobs)



@app.route("/api/v1.0/<start>")
def start_date(start_date):
    session = Session(engine)
    results = session.query(
        (func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs))
        .filter(Measurement.date >= start_date)
        .all()
    )
    session.close()

    start_date_tobs = []
    for min, avg, max in results:
        start_date_tobs_dict = {}
        start_date_tobs_dict["min_temp"] = min
        start_date_tobs_dict["avg_temp"] = avg
        start_date_tobs_dict["max_temp"] = max
        start_date_tobs.append(start_date_tobs_dict) 
    return jsonify(start_date_tobs)


@app.route("/api/v1.0/<start>/<end>")
def start_end_date(start_date, end_date):
    session = Session(engine)
    results = session.query(
        (func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs))
        .filter(Measurement.date >= start_date).filter(Measurement.date <= end_date)
        .all()
    )
    session.close()
  
    start_end_tobs = []
    for min, avg, max in results:
        start_end_tobs_dict = {}
        start_end_tobs_dict["min_temp"] = min
        start_end_tobs_dict["avg_temp"] = avg
        start_end_tobs_dict["max_temp"] = max
        start_end_tobs.append(start_end_tobs_dict) 
    

    return jsonify(start_end_tobs)

if __name__ == '__main__':
    app.run(debug=True)


