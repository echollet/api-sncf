#
# SQLite interface
#

from type_definitions import StopPoints, StopAreas, Lines, Routes

import sqlite3
from sqlite3 import Error

from tqdm import tqdm


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


def db_insert_stop_area(conn, stop_area:tuple):
    sql="""
    INSERT INTO stop_areas (id, name, label)
	VALUES (?,?,?);
    """

    try:
        cur=conn.cursor()
        cur.execute(sql, stop_area)
        conn.commit()
    except Error as e:
        print(e)



def db_insert_line(conn, line:tuple):
    sql="""
    INSERT INTO lines (id, name, code)
	VALUES (?,?,?);
    """

    try:
        cur=conn.cursor()
        cur.execute(sql, line)
        conn.commit()
    except Error as e:
        print(e)


def db_insert_route(conn, route:tuple):
    sql="""
    INSERT INTO routes (id, name, line)
	VALUES (?,?,?);
    """

    try:
        cur=conn.cursor()
        cur.execute(sql, route)
        conn.commit()
    except Error as e:
        print(e)


def db_insert_line_to_route(conn, line_to_route):
    sql="""
    INSERT INTO lnk_line_route (line_id, route_id)
	VALUES (?,?);
    """

    try:
        cur=conn.cursor()
        cur.execute(sql, line_to_route)
        conn.commit()
    except Error as e:
        print(e)    
    return


#
# Interface
#

def db_insert_stop_points(stop_points:StopPoints, dbname:str):
    conn = db_create_connection(dbname)

    with tqdm(total=len(stop_points)) as bar:
        for stop_point in stop_points:
            db_insert_stop_point(conn, (stop_point.id, stop_point.name, stop_point.label, stop_point.type))
            bar.update(1)
    
    return


def db_insert_stop_areas(stop_areas:StopAreas, dbname:str):
    conn = db_create_connection(dbname)

    with tqdm(total=len(stop_areas)) as bar:
        for stop_area in stop_areas:
            db_insert_stop_area(conn, (stop_area.id, stop_area.name, stop_area.label))
            bar.update(1)
    return


def db_insert_lines(lines:Lines, dbname:str):
    conn = db_create_connection(dbname)

    with tqdm(total=len(lines)) as bar:
        for line in lines:
            db_insert_line(conn, (line.id, line.name, line.code))
            bar.update(1)
    return


def db_insert_lines_to_routes(lines_to_routes, dbname:str):
    conn = db_create_connection(dbname)

    with tqdm(total=len(lines_to_routes)) as bar:
        for line_route in lines_to_routes:
            db_insert_line_to_route(conn, line_route)
            bar.update(1)
    return


def db_insert_routes(routes:Routes, dbname:str):
    conn = db_create_connection(dbname)

    with tqdm(total=len(routes)) as bar:
        for route in routes:
            db_insert_route(conn, (route.id, route.name, route.line))
            bar.update(1)
    return