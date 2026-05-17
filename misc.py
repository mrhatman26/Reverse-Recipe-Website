import datetime as dt, re, traceback, sys
from global_vars import deployed, mysql_info
from db_handler_admin import admin_test_server

def pause(message=None):
    if message is None:
        input("(Press ENTER to continue)")
    else:
        input(message)

def get_new_table_id(cursor, table_name):
    cursor.execute("SELECT * FROM " + table_name)
    return len(cursor.fetchall())

def get_time(no_brackets=False, database_time=False):
    current_time = dt.datetime.now()
    if database_time is False:
        if no_brackets is False:
            return str("\n[" + current_time.strftime("%Y.%m.%d at %H:%M:%S") + "]")
        else:
            return str(current_time.strftime("%Y.%m.%d at %H:%M:%S"))
    else:
        return str(current_time.strftime("%Y.%m.%d %H:%M:%S"))
    
def get_current_page(pid, no_results=10):
    current_page = 0
    if pid <= 0:
        return 0
    else:
        while True:
            if pid >= no_results:
                current_page += 1
                pid -= no_results
            else:
                if pid > 0:
                    current_page += 1
                break
        return current_page
    
def test_datetime(date):
    try:
        dt.datetime.strptime(date, "%Y/%m/%d")
        return True
    except:
        return False
    
def get_no_pages(cursor, pid, no_results=10, command=None, no_items=None):
    try:
        if command is not None:
            command = re.sub("SELECT (.*?) FROM", "SELECT count(*) FROM", command)
            command = command.replace(str(pid) + ", ", "0 ,")
            cursor.execute(command)
            fetch = cursor.fetchall()[0][0]
        else:
            fetch = no_items
        no_pages = 0
        if fetch <= 0:
            no_pages =  0
        else:
            while True:
                fetch -= no_results
                no_pages += 1
                if fetch < 1:
                    break
        return no_pages
    except:
        return 0

def get_total_items(command, cursor, is_search=False):
    try:
        command = re.sub("SELECT (.*?) FROM", "SELECT count(*) FROM", command)
        command = command.split(" ORDER")[0]
        if is_search is True:
            command = "SELECT count(*) FROM (" + command + ") AS total"
        cursor.execute(command)
        statement = cursor.statement
        return cursor.fetchall()[0][0]
    except:
        return 0

def to_bool(value, is_no=True):
    if is_no is False:
        return (value == "true" or value is True)
    else:
        return (value == "1" or value == 1)
    
def fprint(value):
    print(value, flush=True)

def set_database_config(args):
    if len(args) < 2:
        fprint("Error: Database info file location not given.\nServer cannot start.")
        pause()
        sys.exit()
    else:
        try:
            database_info_file = open(args[1], "r")
        except:
            fprint("Error: Given database file cannot be opened or might not exist.\nServer cannot start")
            pause()
            sys.exit()
        line_no = 0
        dict_keys = ["user", "password", "host", "port", "database"]
        for line in database_info_file:
            mysql_info[dict_keys[line_no]] = line.strip()
            line_no += 1
        database_info_file.close()
        if admin_test_server() is False:
            fprint("Error: Failed to connect to database, given arguments may be wrong")
            fprint("Please ensure the database config is in the following order:\n1. User\n2. Password\n3. Host\n4. Port\n5. Database")
            fprint("Server cannot start")
            pause()
            sys.exit()
        else:
            fprint("Successfully connected to database")