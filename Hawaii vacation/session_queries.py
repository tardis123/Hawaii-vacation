from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from sqlalchemy.ext.automap import automap_base

engine = create_engine("sqlite:///hawaii.sqlite?check_same_thread=False")

# Reflect database and tables into classes
Base = automap_base()
Base.prepare(engine, reflect=True)

# Save references to classes
Measurements = Base.classes.measurement
Stations = Base.classes.station

# Create session (link) from Python to the DB
session = Session(engine)

""" Functions for both Flask overviews and climate analysis"""
# Calculate date going back one year
def first_date():
    """Calculate date one year back based on most recent measurement"""
    last_date = session.query(func.max(Measurements.date)).scalar()
    first_date  = subtract_year(last_date)
    return (first_date, last_date)

"""Functions for Flask overviews"""

def prcp():
    """Dates and precipitation observations from the last year PER STATION"""
    results = session.query(Stations.name, Measurements.date, Measurements.prcp).\
                            join(Measurements, Stations.station == Measurements.station).\
                            filter(Measurements.date > first_date()[0]).\
                            order_by(Measurements.date).all()
    return results

def stations():
    """Overview of all weather stations"""
    results = session.query(Stations).all()
    return results

def tobs():
    """Temperature observations from the last year"""
    results = session.query(Stations.name, Measurements.date, Measurements.tobs).\
                            join(Measurements, Stations.station == Measurements.station).\
                            filter(Measurements.date> first_date()[0]).\
                            all()

    return results

def period_start():
    """Overall temperature normals as from 2017-01-01"""
    start_date = '2017-01-01'    
    results = session.query(Measurements.date,\
                            func.min(Measurements.tobs).label('min_temp'),\
                            func.round(func.avg(Measurements.tobs)).label('avg_temp'),\
                            func.max(Measurements.tobs).label('max_temp')).\
                            filter(Measurements.date>=start_date).\
                            group_by(Measurements.date).all()
   
    return results

def period_start_end():
    """Overall temperature normals between 2017-01-01 and 2017-07-31"""
    start_date = '2017-01-01'
    end_date = '2017-07-31'    
    results = session.query(Measurements.date,\
                            func.min(Measurements.tobs).label('min_temp'),\
                            func.round(func.avg(Measurements.tobs)).label('avg_temp'),\
                            func.max(Measurements.tobs).label('max_temp')).\
                            filter(Measurements.date>=start_date).\
                            filter(Measurements.date<=end_date).\
                            group_by(Measurements.date).all()
    
    return results    

"""Functions used for climate analysis"""

def subtract_year(any_date):
    """Subtracts one year from any date and returns the result"""
    date = any_date.split("-")
    date = str(int(date[0])-1) + "-" + date[1] + "-" + date[2]
    return date

def prec_last_12_months():
    """Dates and precipitation observations from the last year"""
    results = session.query(Measurements.date, Measurements.prcp).\
                            filter(Measurements.date > first_date()[0]).\
                            order_by(Measurements.date).all()
    return results

def station_count():
    """Number of stations"""
    results= session.query(Stations.station_id).count()
    return results

def station_obs():
    """Observations per station"""
    results = session.query(Stations.name,\
                            func.count(Measurements.station)).\
                            join(Measurements, Stations.station == Measurements.station).\
                            group_by(Measurements.station).order_by(func.count(Measurements.station).desc()).all()
    return results

def year_observation(most_active):
    """Last 12 months of temperature observation data (tobs) for most active station"""
    results  = session.query(Measurements.tobs).\
                                        join(Stations, Stations.station == Measurements.station).\
                                        filter(Measurements.date > first_date()[0]).\
                                        filter(Stations.name == most_active).\
                                        all()
    return results

def calc_temps(start_date, end_date):
    """Calculates min, max and avg temperature for date range"""
    start_year_ago = subtract_year(start_date)
    end_year_ago = subtract_year(end_date)
    
    results = session.query(func.min(Measurements.tobs).label('min_temp'),\
                                    func.avg(Measurements.tobs).label('avg_temp'),\
                                    func.max(Measurements.tobs).label('max_temp')).\
                                    filter(Measurements.date>=start_year_ago).filter(Measurements.date<=end_year_ago).first()
    
    return results.min_temp, round(results.avg_temp), results.max_temp  

def history_rainfall_trip():
    """Rainfall per weather station for previous year's matching dates 
    (based on your trip dates)"""
    trip_start  = input("Enter start for your trip (use YYYY-MM-DD format): ")
    trip_end = input("Enter end for your trip (use YYYY-MM-DD format): ")
    results = session.query(Measurements.station, func.sum(Measurements.prcp)).\
                                        filter(Measurements.date >= subtract_year(trip_start), \
                                        Measurements.date <= subtract_year(trip_end)).\
                                        group_by(Measurements.station).all()

    return results

def daily_normals(any_date):
    #test_date = input("Enter date to calculate daily normals for (use MM-DD format): ")
    results = session.query(func.min(Measurements.tobs).label('min_t'),\
                            func.round(func.avg(Measurements.tobs)).label('avg_t'),\
                            func.max(Measurements.tobs).label('max_t')).\
                            filter(Measurements.date.like(f"%{any_date}")).all()
    return results