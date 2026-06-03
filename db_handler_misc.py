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
        import pyperclip
        pyperclip.copy(cursor.statement)
        no_results = cursor.fetchall()[0][0]
    except Exception as e:
        error_log("localhost", "SYSTEM", "Failed to get the number of results from database command", traceback.format_exc())
    finally:
        return no_results