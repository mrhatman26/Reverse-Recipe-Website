import mysql.connector, traceback
from global_vars import mysql_info, SYSTEM_USER_ID
from db_config import *
from misc import pause
from db_handler_links import link_add_recipe_user, link_check_recipe_user, link_add_ingredient_user, link_check_ingredient_user, link_add_dietary_user, link_check_dietary_user


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
        return None

#Check
def recipe_check_id_exists(recipe_id, database=None, cursor=None, close_connection=True):
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
        cursor.execute("SELECT recipe_id FROM table_recipes WHERE recipe_name = %s", (str(recipe_name),))
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
        print(traceback.format_exc())
        pause()
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
            if link_check_recipe_user(new_recipe_id, database=database, cursor=cursor, close_connection=False) is False:
                link_add_recipe_user(new_recipe_id, SYSTEM_USER_ID, auto_approve=True, database=database, cursor=cursor, close_connection=False)
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
def ingredient_get_name(ingredient_id, database=None, cursor=None, close_connection=True):
    #Returns the ingredient's name using its ID.
    #Arguments:
    #   -ingredient_id (int or str): The ingredient ID to return the name of.
    #   -database (None or database object) [Defaul: None]: The database connection to use. If None, a new connection is created.
    #   -cursor (None or database cursor object) [Default: None]: The cursor to use to interact with the database. If None or if the database is None, a new one is created.
    #   -close_connection (Bool) [Default: True]: If True, the database connection (and the cursor) will be closed. If False, they will be left open.
    #Returns: String (Ingredient Name) or None (Ingredient not found or has no name)
    try:
        if database is None or cursor is None:
            database = mysql.connector.connect(**mysql_info)
            cursor = database.cursor()
        cursor.execute("SELECT ingredient_name FROM table_ingredients WHERE ingredient_id = %s", (str(ingredient_id)),)
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
    
def ingredient_get_id(ingredient_name, database=None, cursor=None, close_connection=True):
    #Returns the ingredients's ID using its name.
    #Arguments:
    #   -ingredient_name (str): The ingredient name to return the ID of.
    #   -database (None or database object) [Defaul: None]: The database connection to use. If None, a new connection is created.
    #   -cursor (None or database cursor object) [Default: None]: The cursor to use to interact with the database. If None or if the database is None, a new one is created.
    #   -close_connection (Bool) [Default: True]: If True, the database connection (and the cursor) will be closed. If False, they will be left open.
    #Returns: String (Ingredient ID) or None (Ingredient not found)
    try:
        if database is None or cursor is None:
            database = mysql.connector.connect(**mysql_info)
            cursor = database.cursor()
        cursor.execute("SELECT ingredient_id FROM table_ingredients WHERE ingredient_name = %s", (str(ingredient_name),))
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
def ingredient_check_id_exists(ingredient_id, database=None, cursor=None, close_connection=True):
    #Checks if the ingredient, specified by the given ID, exists.
    #Arguments:
    #   -ingredient_id (int or str): The ingredient ID to check.
    #   -database (None or database object) [Defaul: None]: The database connection to use. If None, a new connection is created.
    #   -cursor (None or database cursor object) [Default: None]: The cursor to use to interact with the database. If None or if the database is None, a new one is created.
    #   -close_connection (Bool) [Default: True]: If True, the database connection (and the cursor) will be closed. If False, they will be left open.
    #Returns: Boolean (True: ID exists, False: ID does not exist or an error occurred)
    try:
        if database is None or cursor is None:
            database =mysql.connector.connect(**mysql_info)
            cursor = database.cursor()
        cursor.execute("SELECT ingredient_id FROM table_recipes WHERE ingredient_id = %s", (str(ingredient_id)),)
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
    
def ingredient_check_name_exists(ingredient_name, database=None, cursor=None, close_connection=True):
    #Checks if the ingredient, specified by the given name, exists.
    #Arguments:
    #   -ingredient_name (int or str): The ingredient name to check.
    #   -database (None or database object) [Defaul: None]: The database connection to use. If None, a new connection is created.
    #   -cursor (None or database cursor object) [Default: None]: The cursor to use to interact with the database. If None or if the database is None, a new one is created.
    #   -close_connection (Bool) [Default: True]: If True, the database connection (and the cursor) will be closed. If False, they will be left open.
    #Returns: Boolean (True: Name exists, False: Name does not exist or an erro occurred)
    try:
        if database is None or cursor is None:
            database =mysql.connector.connect(**mysql_info)
            cursor = database.cursor()
        cursor.execute("SELECT ingredient_id FROM table_ingredients WHERE ingredient_name = %s", (str(ingredient_name),))
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
def ingredient_add_new(ingredient_data, auto_approve=False, database=None, cursor=None, close_connection=True):
    #Adds a new ingredient to the database using the given data, but only if it doesn't already exist.
    #Arguments:
    #   -ingredient_data (Dict): The ingredient to add. Must be a dictionary containing the ingredient data. The keys must be the same as the column names in the ingredients table.
    #   -auto_approve (Bool) [Default: False]: If True, any recipes will be automatically approved and assigned the approver of SYSTEM. 
    #   -database (None or database object) [Defaul: None]: The database connection to use. If None, a new connection is created.
    #   -cursor (None or database cursor object) [Default: None]: The cursor to use to interact with the database. If None or if the database is None, a new one is created.
    #   -close_connection (Bool) [Default: True]: If True, the database connection (and the cursor) will be closed. If False, they will be left open.
    #Returns: Boolean (True: Ingredient was added succesfully; Ingredient already exists, False: Recipe failed to be added; an error occurred)
    try:
        if database is None or cursor is None:
            database = mysql.connector.connect(**mysql_info)
            cursor = database.cursor()
        if ingredient_check_name_exists(ingredient_data["ingredient_name"], database=database, cursor=cursor, close_connection=False) is False:
            cursor.execute("INSERT INTO table_ingredients(ingredient_name, ingredient_desc, ingredient_isDeleted) VALUES (%s, %s, %s)", (ingredient_data["ingredient_name"], ingredient_data["ingredient_desc"], 0),)
            database.commit()
            if auto_approve is True:
                new_ingredient_id = ingredient_get_id(ingredient_data["ingredient_name"], database=database, cursor=cursor, close_connection=False)
                if link_check_ingredient_user(new_ingredient_id, database=database, cursor=cursor, close_connection=False) is False:
                    link_add_ingredient_user(new_ingredient_id, SYSTEM_USER_ID, auto_approve=True, database=database, cursor=cursor, close_connection=False)
            if close_connection is True:
                cursor.close()
                database.close()
            return True
        else:
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

"""Dietary Info"""
#Get
def dietary_get_name(dietary_id, database=None, cursor=None, close_connection=True):
    #Returns the dietary info's name using its ID (I should have given dietary info a better name...).
    #Arguments:
    #   -dietary_id (int or str): The dietary ID to return the name of.
    #   -database (None or database object) [Defaul: None]: The database connection to use. If None, a new connection is created.
    #   -cursor (None or database cursor object) [Default: None]: The cursor to use to interact with the database. If None or if the database is None, a new one is created.
    #   -close_connection (Bool) [Default: True]: If True, the database connection (and the cursor) will be closed. If False, they will be left open.
    #Returns: String (Dietary Info Name) or None (recipe not found or has no name)
    try:
        if database is None or cursor is None:
            database = mysql.connector.connect(**mysql_info)
            cursor = database.cursor()
        cursor.execute("SELECT dietary_name FROM table_dietary_info WHERE dietary_id = %s", (str(dietary_id)),)
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
    
def dietary_get_id(dietary_name, database=None, cursor=None, close_connection=True):
    #Returns the dietary info's ID using its name (DIETARY INFO NEEDS A BETTER NAME BUT I DON'T WANT TO REFACTOR! And yet somehow, I have a degree...?).
    #Arguments:
    #   -dietary_name (str): The dietary info name to return the ID of.
    #   -database (None or database object) [Defaul: None]: The database connection to use. If None, a new connection is created.
    #   -cursor (None or database cursor object) [Default: None]: The cursor to use to interact with the database. If None or if the database is None, a new one is created.
    #   -close_connection (Bool) [Default: True]: If True, the database connection (and the cursor) will be closed. If False, they will be left open.
    #Returns: String (Dietary Info ID) or None (Dietary Info ID not found)
    try:
        if database is None or cursor is None:
            database = mysql.connector.connect(**mysql_info)
            cursor = database.cursor()
        cursor.execute("SELECT dietary_id FROM table_dietary_info WHERE dietary_name = %s", (str(dietary_name),))
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
def dietary_check_id_exists(dietary_id, database=None, cursor=None, close_connection=True):
    #Checks if the dietary info, specified by the given ID, exists.
    #Arguments:
    #   -dietary_id (int or str): The dietary info ID to check.
    #   -database (None or database object) [Defaul: None]: The database connection to use. If None, a new connection is created.
    #   -cursor (None or database cursor object) [Default: None]: The cursor to use to interact with the database. If None or if the database is None, a new one is created.
    #   -close_connection (Bool) [Default: True]: If True, the database connection (and the cursor) will be closed. If False, they will be left open.
    #Returns: Boolean (True: ID exists, False: ID does not exist or an error occurred)
    try:
        if database is None or cursor is None:
            database =mysql.connector.connect(**mysql_info)
            cursor = database.cursor()
        cursor.execute("SELECT dietary_id FROM table_dietary_info WHERE dietary_id = %s", (str(dietary_id)),)
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
    
def dietary_check_name_exists(dietary_name, database=None, cursor=None, close_connection=True):
    #Checks if the dietary info, specified by the given name, exists.
    #Arguments:
    #   -dietary_name (int or str): The dietary info name to check.
    #   -database (None or database object) [Defaul: None]: The database connection to use. If None, a new connection is created.
    #   -cursor (None or database cursor object) [Default: None]: The cursor to use to interact with the database. If None or if the database is None, a new one is created.
    #   -close_connection (Bool) [Default: True]: If True, the database connection (and the cursor) will be closed. If False, they will be left open.
    #Returns: Boolean (True: Name exists, False: Name does not exist or an erro occurred)
    try:
        if database is None or cursor is None:
            database =mysql.connector.connect(**mysql_info)
            cursor = database.cursor()
        cursor.execute("SELECT dietary_id FROM table_dietary_info WHERE dietary_name = %s", (str(dietary_name),))
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
def dietary_add_new(dietary_data, auto_approve=False, database=None, cursor=None, close_connection=True):
    #Adds new dietary info to the database using the given data, but only if it doesn't already exist.
    #Arguments:
    #   -dietary_data (Dict): The dietary info to add. Must be a dictionary containing the dietary info data. The keys must be the same as the column names in the dietary info table.
    #   -auto_approve (Bool) [Default: False]: If True, any recipes will be automatically approved and assigned the approver of SYSTEM. 
    #   -database (None or database object) [Defaul: None]: The database connection to use. If None, a new connection is created.
    #   -cursor (None or database cursor object) [Default: None]: The cursor to use to interact with the database. If None or if the database is None, a new one is created.
    #   -close_connection (Bool) [Default: True]: If True, the database connection (and the cursor) will be closed. If False, they will be left open.
    #Returns: Boolean (True: Dietary info was added succesfully; Dietary info already exists, False: Dietary info failed to be added; an error occurred)
    try:
        if database is None or cursor is None:
            database = mysql.connector.connect(**mysql_info)
            cursor = database.cursor()
        if dietary_check_name_exists(dietary_data["dietary_name"], database=database, cursor=cursor, close_connection=False) is False:
            cursor.execute("INSERT INTO table_dietary_info(dietary_name, dietary_desc, dietary_isDeleted) VALUES (%s, %s, %s)", (dietary_data["dietary_name"], dietary_data["dietary_desc"], 0),)
            database.commit()
            if auto_approve is True:
                new_dietary_id = dietary_get_id(dietary_data["dietary_name"], database=database, cursor=cursor, close_connection=False)
                if link_check_dietary_user(new_dietary_id, database=database, cursor=cursor, close_connection=False) is False:
                    link_add_dietary_user(new_dietary_id, SYSTEM_USER_ID, auto_approve=True, database=database, cursor=cursor, close_connection=False)
            if close_connection is True:
                cursor.close()
                database.close()
            return True
        else:
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