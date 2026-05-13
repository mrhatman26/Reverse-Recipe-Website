from global_vars import mysql_info
def get_db_config(deployed):
    db_config = {}
    if deployed:
        db_config = {
            'user': 'root',
            'password': mysql_info["password"],
            'host': 'localhost',
            'port': 1234,
            'database': 'recipedatabase'
        }
    else:
        db_config = {
            'user': 'root',
            'password': mysql_info["password"],
            'host': 'localhost',
            'port': 3306,
            'database': 'recipedatabase'
        }
    return db_config