import mysql.connector
from global_vars import mysql_info
from db_config import *

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
        cursor.execute("SELECT recipe_id FROM table_recipes WHERE recipe_name = %s", (str(recipe_name)),)
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
        cursor.execute("INSERT INTO table_recipes VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (recipe_data["id"], recipe_data["name"], recipe_data["author"], recipe_data["prep"], recipe_data["cook_time"], recipe_data["serve_size"], recipe_data["method"], recipe_data["type"], recipe_data["scraped"], recipe_data["source_url"], recipe_data["isDeleted"]),)
        database.commit()
        if auto_approve is True:
            cursor.execute("")
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