import mysql.connector, hashlib
from db_config import *
from misc import fprint, pause
from global_vars import deployed

def string_hash(text):
    text = text.encode('utf-8')
    hash = hashlib.sha256()
    hash.update(text)
    return hash.hexdigest()

#Checks/Login    
def user_check_exists(username):
    try:
        database = mysql.connector.connect(**get_db_config(deployed))
        cursor = database.cursor()
        cursor.execute("SELECT user_id FROM table_users WHERE user_name = %s", (str(username),))
        fetch = cursor.fetchall()
        cursor.close()
        database.close()
        if len(fetch) > 0:
            return True
        else:
            return False
    except:
        if cursor is not None:
            cursor.close()
        if database is not None:
            database.close()
        return False
    
def user_check_reconfirm(user_id):
    try:
        user = []
        database = mysql.connector.connect(**get_db_config(deployed))
        cursor = database.cursor()
        cursor.execute("SELECT user_id, user_name, user_isMod, user_isAdmin FROM table_users WHERE user_id = %s", (str(user_id),))
        fetch = cursor.fetchall()
        cursor.close()
        database.close()
        if len(fetch) > 0:
            for item in fetch:
                user.append(item[0])
                user.append(item[1])
                user.append(item[2])
                user.append(item[3])
            return user
        else:
            return []
    except:
        if cursor is not None:
            cursor.close()
        if database is not None:
            database.close()
        return []

def user_login_passcheck(userdata):
    try:
        database = mysql.connector.connect(**get_db_config(deployed))
        cursor = database.cursor()
        cursor.execute("SELECT user_pass FROM table_users WHERE user_name = %s", (str(userdata["user_name"]),))
        fetch = cursor.fetchall()[0][0]
        cursor.close()
        database.close()
        if string_hash(userdata["user_password"]) == fetch:
            return True
        else:
            return False
    except:
        if cursor is not None:
            cursor.close()
        if database is not None:
            database.close()
        return False
    
def user_check_admin(username):
    try:
        database = mysql.connector.connect(**get_db_config(deployed))
        cursor = database.cursor()
        cursor.execute("SELECT user_isMod, user_isAdmin FROM table_users WHERE user_name = %s", (str(username),))
        fetch = cursor.fetchall()[0]
        cursor.close()
        database.close()
        return (bool(fetch[0]), bool(fetch[1]))
    except:
        if cursor is not None:
            cursor.close()
        if database is not None:
            database.close()
        return (False, False)
    
#Get
def user_get_id(username):
    try:
        database = mysql.connector.connect(**get_db_config(deployed))
        cursor = database.cursor()
        cursor.execute("SELECT user_id FROM table_users WHERE user_name = %s", (str(username),))
        fetch = cursor.fetchall()[0][0]
        cursor.close()
        database.close()
        return fetch
    except:
        if cursor is not None:
            cursor.close()
        if database is not None:
            database.close()
        return None
    
def user_get_username(user_id):
    try:
        database = mysql.connector.connect(**get_db_config(deployed))
        cursor = database.cursor()
        cursor.execute("SELECT user_name FROM table_users WHERE user_id = %s", (str(user_id),))
        fetch = cursor.fetchall()
        cursor.close()
        database.close()
        if len(fetch) > 0:
            return fetch[0][0]
        else:
            return None
    except:
        if cursor is not None:
            cursor.close()
        if database is not None:
            database.close()
        return None
    
def user_get_all():
    try:
        user_list = []
        database = mysql.connector.connect(**get_db_config(deployed))
        cursor = database.cursor()
        cursor.execute("SELECT user_id, user_name, user_desc, user_email, user_isAdmin, user_isMod FROM table_users WHERE user_id >= 0")
        for item in cursor.fetchall():
            if item[1] is not None:
                if item[1].isspace or item[1] == "":
                    item[1] == None
            user_list.append({
                "user_id": item[0],
                "user_name": item[1],
                "user_desc": item[2],
                "user_email": item[3],
                "user_isAdmin": item[4],
                "user_isMod": item[5]
            })
        cursor.close()
        database.close()
        return user_list
    except:
        if cursor is not None:
            cursor.close()
        if database is not None:
            database.close()
        return []
    
def user_single_get_all(user_id):
    try:
        database = mysql.connector.connect(**get_db_config(deployed))
        cursor = database.cursor()
        cursor.execute("SELECT user_id, user_email, user_desc FROM table_users WHERE user_id = %s", (user_id,))
        fetch = cursor.fetchall()
        cursor.close()
        database.close()
        if len(fetch) > 0:
            fetch = fetch[0]
            return {
                "user_id": fetch[0],
                "user_email": fetch[1],
                "user_desc": fetch[2]
            }
        else:
            return None
    except:
        if cursor is not None:
            cursor.close()
        if database is not None:
            database.close()
        return None
    
def user_get_email(user_id):
    try:
        database = mysql.connector.connect(**get_db_config(deployed))
        cursor = database.cursor()
        cursor.execute("SELECT user_email FROM table_users WHERE user_id = %s", (user_id,))
        fetch = cursor.fetchall()
        cursor.close()
        database.close()
        if len(fetch) > 0:
            return fetch[0][0]
        else:
            return None
    except:
        if cursor is not None:
            cursor.close()
        if database is not None:
            database.close()
        return None
    
#Add/Modify
def user_add_new(new_userdata, set_mod=False, set_admin=False):
    try:
        if set_admin is True:
            set_mod = True
        database = mysql.connector.connect(**get_db_config(deployed))
        cursor = database.cursor()
        new_userdata["user_password"] = string_hash(new_userdata["user_password"])
        cursor.execute("INSERT INTO table_users (user_name, user_pass, user_email, user_desc, user_pfp, user_isAdmin, user_isMod) VALUES (%s, %s, %s, %s, %s, %s, %s)", (new_userdata["user_name"], new_userdata["user_password"], new_userdata["user_email"], None, None, set_admin, set_mod,))
        database.commit()
        cursor.close()
        database.close()
        return True
    except:
        if cursor is not None:
            cursor.close()
        if database is not None:
            database.close()
        return False

def user_modify_username(user_id, new_username):
    try:
        database = mysql.connector.connect(**get_db_config(deployed))
        cursor = database.cursor()
        cursor.execute("UPDATE table_users SET user_name = %s WHERE user_id = %s", (new_username, user_id,))
        database.commit()
        cursor.close()
        database.close()
        return True
    except:
        if cursor is not None:
            cursor.close()
        if database is not None:
            database.close()
        return False
    
def user_modify_email(user_id, new_email):
    try:
        database = mysql.connector.connect(**get_db_config(deployed))
        cursor = database.cursor()
        cursor.execute("UPDATE table_users SET user_email = %s WHERE user_id = %s", (new_email, user_id,))
        database.commit()
        cursor.close()
        database.close()
        return True
    except:
        if cursor is not None:
            cursor.close()
        if database is not None:
            database.close()
        return False
    
def user_delete(user_id):
    try:
        database = mysql.connector.connect(**get_db_config(deployed))
        cursor = database.cursor()
        tag_void_user_link(user_id, cursor=cursor, database=database)
        game_void_user_link(user_id, cursor=cursor, database=database)
        devpub_void_user_link(user_id, cursor=cursor, database=database)
        update_void_user_link(user_id, cursor=cursor, database=database)
        cursor.execute("DELETE FROM table_users WHERE user_id = %s", (user_id,))
        database.commit()
        cursor.close()
        database.close()
        return True
    except:
        if cursor is not None:
            cursor.close()
        if database is not None:
            database.close()
        return False