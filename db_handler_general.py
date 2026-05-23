import mysql.connector, traceback
from global_vars import mysql_info, SYSTEM_USER_ID, DEFAULT_RECIPE_NO
from db_config import *
from misc import pause
from db_handler_links import link_add_recipe_user, link_check_recipe_user, link_add_ingredient_user, link_check_ingredient_user, link_add_dietary_user, link_check_dietary_user
from action_logger import error_log


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
        fetch = cursor.fetchall()[0][0].replace("_", " ").title()
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
        recipe_name = recipe_name.replace(" ", "_")
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
    
def recipe_get_all_partial(starting_id, no_results=DEFAULT_RECIPE_NO, search="", search_type=0):
    #Gets a partial selection of recipes from the database.
    #Arguments:
    #   -starting_id (Int): The ID of the first recipe to return. The rest of the returned recipes will be the ones after the specified recipe ID (Why is this so hard to explain?).
    #   -no_results (Int) [Default: DEFAULT_RECIPE_NO]: The number of recipes to return including the recipe specified by starting_id. 
    #   -search (Str) [Default: None]: The search parameters to perform when selecting recipes. Each value must be seperated by a plus (+).
    #   -search_type (Int) [Default: 0]: The type of search being done. 0 is searching for recipes with specified ingredients, 1 is searching for recipes with specified dietary info, 2 is searching for recipes by name and 3 is searching by recipe type.
    #Returns: Tuple:
    #   0: List of recipes returned from database.
    #   1: Number of pages to contain all recipes for pagination.
    #   2: Total number of recipes in the database (Ignoring the DELETED recipe with ID of -1).
    recipes = []
    database = mysql.connector.connect(**mysql_info)
    cursor = database.cursor()
    fetch = []
    try:
        if search.isspace() is True or search == "":
            cursor.execute("SELECT table_recipes.recipe_id, table_recipes.recipe_name, table_recipes.recipe_author, table_recipes.recipe_type FROM table_recipes INNER JOIN link_recipe_user ON table_recipes.recipe_id=link_recipe_user.recipe_id WHERE link_recipe_user.link_isApproved = 1 AND table_recipes.recipe_isDeleted = 0 ORDER BY table_recipes.recipe_id DESC LIMIT %s, %s", (starting_id, no_results + 1))
            fetch = cursor.fetchall()
        else:
            pass
        for recipe in fetch:
            recipes.append({
                "recipe_id": recipe[0],
                "recipe_name": recipe[1].replace("_", " ").title(),
                "recipe_author": recipe[2].replace("_", " ").title(),
                "recipe_type": recipe[3].replace("_", " ").title()
            })
        statement = cursor.statement
    except Exception as e:
        error_log("localhost", "SYSTEM", "An error occurred while retrieving recipe data", traceback.format_exc())
    finally:
        statement = cursor.statement
        #ToDo: Have all spaces in recipe names, recipe types, ingredient names and dietary info names be replaced with spaces.
        #ToDo2: Calculate number of pages and total number of recipes for pagination!
        no_pages = 1
        total_recipes = 10
        cursor.close()
        database.close()
        return (recipes, no_pages, total_recipes)
    
def recipe_get_individual_info(recipe_id):
    #Returns data for the specified recipe
    #Arguments:
    #   -recipe_id: The ID of the recipe to get the data forl.
    #Returns: Dict (Contains recipe info with they keys being the column names of table_recipe)
    recipe_info = {}
    database = mysql.connector.connect(**mysql_info)
    cursor = database.cursor()
    try:
        cursor.execute("SELECT * FROM table_recipes WHERE recipe_id = %s", (recipe_id,))
        fetch = cursor.fetchall()
        if len(fetch) > 0:
            recipe_info = {
                "recipe_id": fetch[0][0],
                "recipe_name": fetch[0][1].replace("_", " ").title(),
                "recipe_author": fetch[0][2].replace("_", " ").title(),
                "recipe_prep": fetch[0][3],
                "recipe_cook_time": fetch[0][4],
                "recipe_serve_size": fetch[0][5],
                "recipe_method": fetch[0][6],
                "recipe_type": fetch[0][7].replace("_", " ").title(),
                "recipe_scraped": fetch[0][8],
                "recipe_source_url": fetch[0][9],
                "recipe_isDeleted": fetch[0][10],
            }
    except Exception as e:
        error_log("localhost", "SYSTEM", "An error occurred while retrieving individual recipe data", traceback.format_exc())
    finally:
        cursor.close()
        database.close()
        return recipe_info

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
        recipe_name = recipe_name.replace(" ", "_").lower()
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
        recipe_data["recipe_name"] = recipe_data["recipe_name"].replace(" ", "_").lower()
        recipe_data["recipe_author"] = recipe_data["recipe_author"].replace(" ", "_").lower()
        recipe_data["recipe_type"] = recipe_data["recipe_type"].replace(" ", "_").lower()
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
        fetch = cursor.fetchall()[0][0].replace("_", " ").title()
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
        ingredient_name = ingredient_name.replace(" ", "_").lower()
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
        ingredient_name = ingredient_name.replace(" ", "_").lower()
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
        ingredient_data["ingredient_name"] = ingredient_data["ingredient_name"].replace(" ", "_").lower()
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
        fetch = cursor.fetchall()[0][0].replace("_", " ").title()
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
        dietary_name = dietary_name.replace(" ", "_").lower()
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
        dietary_name = dietary_name.replace(" ", "_").lower()
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
        dietary_data["dietary_name"] = dietary_data["dietary_name"].replace(" ", "_").lower()
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