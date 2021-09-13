import traceback
import cx_Oracle

conn=None
try:
    conn=cx_Oracle.connect("mouzikka/music@127.0.0.1/xe")
    print("Connection done successfully!")

except cx_Oracle.DatabaseError:
    print("DB Error!")
    print(traceback.format_exc())
finally:
    if conn is not None:
        conn.close()
