import mysql.connector, traceback, re
from global_vars import mysql_info, DEFAULT_RECIPE_NO
from action_logger import error_log

def get_no_pages(cursor, command, starting_point, no_results=DEFAULT_RECIPE_NO):
    no_pages = 0
    try:
        command = re.sub("SELECT (.*?) FROM", "SELECT count(*) FROM", command)
        command = command.replace(str(starting_point) + ", ", "0 ,")
        cursor.execute(command)
        fetch = cursor.fetchall()[0][0]
        if fetch > 0:
            while fetch > 0:
                fetch -= no_results
                no_pages += 1
    except Exception as e:
        error_log("localhost", "SYSTEM", "Failed to get the number of pages for pagination", traceback.format_exc())
    finally:
        return no_pages
    
def get_no_results(cursor, command, is_search):
    no_results = 0
    try:
        command = re.sub("SELECT (.*?) FROM", "SELECT count(*) FROM", command)
        command = command.split(" ORDER")[0]
        if is_search is True:
            command = "SELECT count(*) FROM (" + command + ") AS total"
        cursor.execute(command)
        no_results = cursor.fetchall()[0][0]
    except Exception as e:
        error_log("localhost", "SYSTEM", "Failed to get the number of results from database command", traceback.format_exc())
    finally:
        return no_results
    
def search_all_names(search):
    closest_results = ""
    database = None
    cursor = None
    try:
        database = mysql.connector.connect(**mysql_info)
        cursor = database.cursor()
        search = "%" + search + "%"
        cursor.execute("SELECT ingredient_name FROM table_ingredients WHERE ingredient_name LIKE %s UNION SELECT dietary_name FROM table_dietary_info WHERE dietary_name LIKE %s LIMIT 5", (search, search,))
        for result in cursor.fetchall():
            if closest_results == "":
                closest_results = result[0]
            else:
                closest_results += "|" + result[0]
        import pyperclip
        pyperclip.copy(cursor.statement)
    except Exception as e:
        error_log("localhost", "SYSTEM", "Failed to get closest database names to search", traceback.format_exc())
    finally:
        if cursor is not None:
            cursor.close()
        if database is not None:
            database.close()
        return closest_results