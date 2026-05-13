import mysql.connector
from global_vars import deployed, mysql_info
from db_config import *

def admin_test_server():
    try:
        database = mysql.connector.connect(**mysql_info)
        cursor = database.cursor()
        cursor.execute("SELECT * FROM table_users")
        fetch = cursor.fetchall()
        cursor.close()
        database.close()
        return True
    except:
        return False