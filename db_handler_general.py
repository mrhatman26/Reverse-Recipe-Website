import mysql.connector, traceback
from global_vars import mysql_info, SYSTEM_USER_ID
from db_config import *
from misc import get_time, pause


"""Recipes"""
#Get
def recipe_get_name(recipe_id, database=None, cursor=None, close_connection=True):
    #Returns the recipe's name using its ID.
    #Arguments:
    #   -recipe_id (int or str): The recipe ID to return the name of.
    #   -database (None or database object) [Defaul: None]: The database connection to use. If None, a new connection is created.
    #   -cursor (None or database cursor object) [Default: None]: The cursor to use to interact with the database. If None or if the database is None, a new one is created.
    #   -close_connection (Bool) [Default: True]: If True, the database connection (and the cursor) will be closed. If False, they will be left open.
    #Returns: String (Recipe Name) or None (recipe not found or has no name)
    try:
        if database is None or cursor is None:
            database = mysql.connector.connect(**mysql_info)
            cursor = database.cursor()
        cursor.execute("SELECT recipe_name FROM table_recipes WHERE recipe_id = %s", (str(recipe_id)),)
        fetch = cursor.fetchall()[0][0]
        if close_connection is True:
            cursor.close()
            database.close()
        return fetch
    except:
        if close_connection is True:
            if cursor is not None:
                cursor.close()
            if database is not None:
                database.close()
        return None
    
def recipe_get_id(recipe_name, database=None, cursor=None, close_connection=True):
    #Returns the recipe's ID using its name.
    #Arguments:
    #   -recipe_name (str): The recipe name to return the ID of.
    #   -database (None or database object) [Defaul: None]: The database connection to use. If None, a new connection is created.
    #   -cursor (None or database cursor object) [Default: None]: The cursor to use to interact with the database. If None or if the database is None, a new one is created.
    #   -close_connection (Bool) [Default: True]: If True, the database connection (and the cursor) will be closed. If False, they will be left open.
    #Returns: String (Recipe ID) or None (Recipe not found)
    try:
        if database is None or cursor is None:
            database = mysql.connector.connect(**mysql_info)
            cursor = database.cursor()
        cursor.execute("SELECT recipe_id FROM table_recipes WHERE recipe_name = %s", (str(recipe_name),))
        fetch = cursor.fetchall()[0][0]
        if close_connection is True:
            cursor.close()
            database.close()
        return fetch
    except:
        if close_connection is True:
            if cursor is not None:
                cursor.close()
            if database is not None:
                database.close()
        print(traceback.format_exc())
        print(recipe_name)
        print(type(recipe_name))
        pause()
        return None

#Check
def recipe_check_id_exists(recipe_id, database=None, cursor=None, close_connection=True):
    #This function may be redundant as you could instead use recipe_get_id or recipe_get_name and simply making sure they do not return None. Oh well.
    #Checks if the recipe, specified by the given ID, exists.
    #Arguments:
    #   -recipe_id (int or str): The recipe ID to check.
    #   -database (None or database object) [Defaul: None]: The database connection to use. If None, a new connection is created.
    #   -cursor (None or database cursor object) [Default: None]: The cursor to use to interact with the database. If None or if the database is None, a new one is created.
    #   -close_connection (Bool) [Default: True]: If True, the database connection (and the cursor) will be closed. If False, they will be left open.
    #Returns: Boolean (True: ID exists, False: ID does not exist or an error occurred)
    try:
        if database is None or cursor is None:
            database =mysql.connector.connect(**mysql_info)
            cursor = database.cursor()
        cursor.execute("SELECT recipe_id FROM table_recipes WHERE recipe_id = %s", (str(recipe_id)),)
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
        return False
    
def recipe_check_name_exists(recipe_name, database=None, cursor=None, close_connection=True):
    #This function may be redundant as you could instead use recipe_get_id or recipe_get_name and simply making sure they do not return None. Oh well.
    #Checks if the recipe, specified by the given name, exists.
    #Arguments:
    #   -recipe_name (int or str): The recipe name to check.
    #   -database (None or database object) [Defaul: None]: The database connection to use. If None, a new connection is created.
    #   -cursor (None or database cursor object) [Default: None]: The cursor to use to interact with the database. If None or if the database is None, a new one is created.
    #   -close_connection (Bool) [Default: True]: If True, the database connection (and the cursor) will be closed. If False, they will be left open.
    #Returns: Boolean (True: Name exists, False: Name does not exist or an erro occurred)
    try:
        if database is None or cursor is None:
            database =mysql.connector.connect(**mysql_info)
            cursor = database.cursor()
        cursor.execute("SELECT recipe_id FROM table_recipes WHERE recipe_name = %s", (str(recipe_name)),)
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
        return False

#Add
def recipe_add_new(recipe_data, auto_approve=False, database=None, cursor=None, close_connection=True):
    #Adds a new recipe to the database using the given data.
    #Arguments:
    #   -recipe_data (Dict): The recipe to add. Must be a dictionary containing the recipe data. The keys must be the same as the column names in the recipe table.
    #   -auto_approve (Bool) [Default: False]: If True, any recipes will be automatically approved and assigned the approver of SYSTEM. 
    #   -database (None or database object) [Defaul: None]: The database connection to use. If None, a new connection is created.
    #   -cursor (None or database cursor object) [Default: None]: The cursor to use to interact with the database. If None or if the database is None, a new one is created.
    #   -close_connection (Bool) [Default: True]: If True, the database connection (and the cursor) will be closed. If False, they will be left open.
    #Returns: Boolean (True: Recipe was added succesfully, False: Recipe failed to be added; an error occurred)
    try:
        if database is None or cursor is None:
            database = mysql.connector.connect(**mysql_info)
            cursor = database.cursor()
        cursor.execute("INSERT INTO table_recipes(recipe_name, recipe_author, recipe_prep, recipe_cook_time, recipe_serve_size, recipe_method, recipe_type, recipe_scraped, recipe_source_url, recipe_isDeleted) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (recipe_data["recipe_name"], recipe_data["recipe_author"], recipe_data["recipe_prep"], recipe_data["recipe_cook_time"], recipe_data["recipe_serve_size"], recipe_data["recipe_method"], recipe_data["recipe_type"], recipe_data["recipe_scraped"], recipe_data["recipe_source_url"], recipe_data["recipe_isDeleted"]),)
        database.commit()
        if auto_approve is True:
            new_recipe_id = recipe_get_id(recipe_data["recipe_name"], database=database, cursor=cursor, close_connection=False)
            cursor.execute("INSERT INTO link_recipe_user VALUES(%s, %s, %s, %s, %s, %s, %s)", (new_recipe_id, SYSTEM_USER_ID, get_time(no_brackets=True), 1, get_time(no_brackets=True), SYSTEM_USER_ID, None),)
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
        return False


#Update

#Delete

"""Ingredients"""
#Get

#Check

#Add

#Update

#Delete

"""Dietary Info"""
#Get

#Check

#Add

#Update

#Delete