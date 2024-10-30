from performance_script import *
import sqlite3

with sqlite3.connect('database/database.db') as conn:
    cur = conn.cursor()
    try:
        fetch_all_rows(cur)
    finally:
        cur.close()