#!/usr/bin/python
import psycopg2
from psycopg2.extras import DictCursor

from db_config import config

def runSQL(query):
    """ Connect to the PostgreSQL database server """
    conn = None
    result = ""
    try:
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        conn = psycopg2.connect(**params, cursor_factory=DictCursor)
		
        # create a cursor
        cur = conn.cursor()
        
	# execute a statement
        cur.execute(query)
        result = cur.fetchall()

	# close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        logfile = open('error.log','a+')
        print(error, file=logfile)
        logfile.close()
    finally:
        if conn is not None:
            conn.close()
    return result
