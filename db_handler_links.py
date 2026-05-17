import mysql.connector, traceback
from global_vars import mysql_info, SYSTEM_USER_ID
from db_config import *
from misc import get_time

#Check
def link_check_recipe_user(recipe_id, database=None, cursor=None, close_connection=True):
    #Checks if the specified recipe is linked to a user or not.
    #Arguments:
    #   -recipe_id: The recipe to check.
    #   -database (None or database object) [Defaul: None]: The database connection to use. If None, a new connection is created.
    #   -cursor (None or database cursor object) [Default: None]: The cursor to use to interact with the database. If None or if the database is None, a new one is created.
    #   -close_connection (Bool) [Default: True]: If True, the database connection (and the cursor) will be closed. If False, they will be left open.
    #Returns: Boolean (True: The recipe is linked to a user, False: The recipe is not linked to a user; an error occurred)
    try:
        if database is None or cursor is None:
            database = mysql.connector.connect(**mysql_info)
            cursor = database.cursor()
        cursor.execute("SELECT recipe_id FROM link_recipe_user WHERE recipe_id = %s", (str(recipe_id),))
        fetch = cursor.fetchall()
        if close_connection is True:
            cursor.close()
            database.close()
        if len(fetch) > 0:
            return True
        else:
            return False
    except:
        if close_connection is True:
            if cursor is not None:
                cursor.close()
            if database is not None:
                database.close()
        import traceback
        print(traceback.format_exc())
        input("(Press ENTER to continue)")
        return False
        

#Add
def link_add_recipe_user(recipe_id, user_id, auto_approve=False, database=None, cursor=None, close_connection=True):
    #Links a recipe to a user. The linked user is then considered to be the user that originally added it. A link must be approved by a moderator or an admin. Auto approve does this automatically.
    #Arguments:
    #   -recipe_id: The recipe to link the user to.
    #   -user_id: The user to link to the recipe.
    #   -auto_approve (Bool) [Default: False]: If True, any recipes will be automatically approved and assigned the approver of SYSTEM. 
    #   -database (None or database object) [Defaul: None]: The database connection to use. If None, a new connection is created.
    #   -cursor (None or database cursor object) [Default: None]: The cursor to use to interact with the database. If None or if the database is None, a new one is created.
    #   -close_connection (Bool) [Default: True]: If True, the database connection (and the cursor) will be closed. If False, they will be left open.
    #Returns: Boolean (True: Recipe was linked to user succesfully, False: Recipe failed to be linked; an error occurred)
    try:
        if database is None or cursor is None:
            database = mysql.connector.connect(**mysql_info)
            cursor = database.cursor()
        cursor.execute("INSERT INTO link_recipe_user(recipe_id, user_id, link_date) VALUES(%s, %s, %s)", (recipe_id, user_id, get_time(database_time=True)),)
        database.commit()
        if auto_approve is True:
            cursor.execute("UPDATE link_recipe_user SET link_isApproved = 1, approve_date = %s, approve_user_id = %s WHERE recipe_id = %s AND user_id = %s", (get_time(database_time=True), SYSTEM_USER_ID, recipe_id, user_id))
            database.commit()
        if close_connection is True:
            cursor.close()
            database.close()
        return True
    except:
        if close_connection is True:
            if cursor is not None:
                cursor.close()
            if database is not None:
                database.close()
        import traceback
        print(traceback.format_exc())
        input("(Press ENTER to continue)")
        return False