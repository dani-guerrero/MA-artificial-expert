import time
import db_queries as q

SLEEP_TIME = 3
while True:
    q.connect() 
    time.sleep(SLEEP_TIME)
