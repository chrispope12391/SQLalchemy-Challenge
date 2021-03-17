import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

######################################
#Database setup
######################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect on existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

######################################
#Flask Setup
######################################
app = Flask(__name__)

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        "/api/v1.0/<start>/<end>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of precipitation data"""
    # Query all passengers
    results = session.query(Measurement.date, Measurement.prcp).all()

    session.close()

    # Convert list of tuples into normal list
    all_precip = []
    for date, prcp in results:
        measurement_dict={}
        measurement_dict['date'] = date
        measurement_dict['prcp'] = prcp
        all_precip.append(measurement_dict)

    return jsonify(all_precip)


@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of precipitation data"""
    # Query all passengers
    results = session.query(Station.station).all()

    session.close()

    all_stations = list(np.ravel(results))

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of precipitation data"""
    # Query all passengers
    results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date > '2016-08-22').all()

    session.close()

    all_tobs = list(np.ravel(results))

    return jsonify(all_tobs)


@app.route("/api/v1.0/<start>")
def start(start):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    sel = [Measurement.date,
        func.min(Measurement.tobs),
        func.max(Measurement.tobs),
        func.avg(Measurement.tobs)]

    """Return a list of precipitation data"""
    # Query all passengers
    results = session.query(*sel).\
        filter(Measurement.date >= start).\
        group_by(Measurement.date).\
        order_by(Measurement.date).all()

    session.close()

    start_tobs = list(np.ravel(results))

    return jsonify(start_tobs)


@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    sel = [Measurement.date,
    func.min(Measurement.tobs),
    func.max(Measurement.tobs),
    func.avg(Measurement.tobs)]

    """Return a list of precipitation data"""
    # Query all passengers
    results = session.query(*sel).\
    filter(Measurement.date > start).\
    filter(Measurement.date < end).\
    group_by(Measurement.date).\
    order_by(Measurement.date).all()

    session.close()

    start_end_tobs = list(np.ravel(results))

    return jsonify(start_end_tobs)


if __name__ == '__main__':
    app.run(debug=True)
