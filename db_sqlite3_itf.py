#
# SQLite interface
#

from type_definitions import StopPoint, StopPoints

import sqlite3
from sqlite3 import Error

def db_create_connection(db_file:str):
    """ create connection to database """
    conn=None
    try:
        conn=sqlite3.connect(db_file)
        print(sqlite3.version)
    except Error as e:
        print(e)

    return conn


def db_insert_stop_point(conn, stop_point):
    sql="""
    INSERT INTO stop_points (id, name, label, id_type)
	VALUES (?,?,?,?);
    """

    #(id,name,label,type) = stop_point
    try:
        cur=conn.cursor()
        cur.execute(sql, stop_point)
        conn.commit()
    except Error as e:
        print(e)


def db_insert_stop_points(stop_points:StopPoints, dbname:str):
    conn = db_create_connection(dbname)

    for stop_point in stop_points.train_stops:
        db_insert_stop_point(conn, (stop_point.id, stop_point.name, stop_point.label, 1))
    for stop_point in stop_points.long_dist_train_stops:
        db_insert_stop_point(conn, (stop_point.id, stop_point.name, stop_point.label, 2))
    return