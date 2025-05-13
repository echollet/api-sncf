#
# SQLite interface
#


import sqlite3
from sqlite3 import Error

def create_connection(db_file:str):
    """ create connection to database """
    conn=None
    try:
        conn=sqlite3.connect(db_file)
        print(sqlite3.version)
    except Error as e:
        print(e)

    return conn


def insert_train_stop(conn, stop_point):
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