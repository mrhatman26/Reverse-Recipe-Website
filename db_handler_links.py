import mysql.connector, traceback
from global_vars import mysql_info, SYSTEM_USER_ID
from db_config import *
from misc import get_time

'''Recipes'''
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
        return False
    
def link_check_recipe_ingredient(recipe_id, ingredient_id, database=None, cursor=None, close_connection=True):
    #Checks if the specified recipe is linked to the specified ingredient or not.
    #Arguments:
    #   -recipe_id: The recipe to check.
    #   -ingredient_id: The ingredient to check.
    #   -database (None or database object) [Defaul: None]: The database connection to use. If None, a new connection is created.
    #   -cursor (None or database cursor object) [Default: None]: The cursor to use to interact with the database. If None or if the database is None, a new one is created.
    #   -close_connection (Bool) [Default: True]: If True, the database connection (and the cursor) will be closed. If False, they will be left open.
    #Returns: Boolean (True: The recipe is linked to an ingredient, False: The recipe is not linked to an ingredient; an error occurred)        
    try:
        if database is None or cursor is None:
            database = mysql.connector.connect(**mysql_info)
            cursor = database.cursor()
        cursor.execute("SELECT recipe_id FROM link_recipe_ingredient WHERE recipe_id = %s AND ingredient_id = %s", (str(recipe_id), str(ingredient_id),))
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
    
def link_check_recipe_dietary(recipe_id, dietary_id, database=None, cursor=None, close_connection=True):
    #Checks if the specified recipe is linked to the specified dietary info or not.
    #Arguments:
    #   -recipe_id: The recipe to check.
    #   -dietary_id: The dietary info to check.
    #   -database (None or database object) [Defaul: None]: The database connection to use. If None, a new connection is created.
    #   -cursor (None or database cursor object) [Default: None]: The cursor to use to interact with the database. If None or if the database is None, a new one is created.
    #   -close_connection (Bool) [Default: True]: If True, the database connection (and the cursor) will be closed. If False, they will be left open.
    #Returns: Boolean (True: The recipe is linked to the dietary info, False: The recipe is not linked to the dietary info; an error occurred)        
    try:
        if database is None or cursor is None:
            database = mysql.connector.connect(**mysql_info)
            cursor = database.cursor()
        cursor.execute("SELECT recipe_id FROM link_recipe_dietary WHERE recipe_id = %s AND dietary_id = %s", (str(recipe_id), str(dietary_id),))
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
    
#Get
def link_get_recipe_user_id(recipe_id):
    #Returns the user ID of the user who added the specified recipe.
    #Arguements:
    #   -recipe_id (String): The recipe_id to check
    #Returns: String (User ID)
    database = None
    cursor = None
    try:
        database = mysql.connector.connect(**mysql_info)
        cursor = database.cursor()
        cursor.execute("SELECT table_users.user_id FROM table_users INNER JOIN link_recipe_user ON table_users.user_id=link_recipe_user.user_id WHERE link_recipe_user.recipe_id = %s", (recipe_id,))
        fetch = cursor.fetchall()
        cursor.close()
        database.close()
        return fetch[0][0]
    except:
        if cursor is not None:
            cursor.close()
        if database is not None:
            database.close()
        return None
    
def link_get_recipe_ingredients(recipe_id, return_ingredient_names=True):
    #Returns the name or IDs of the ingredients linked to the specified recipe.
    #Arguments:
    #   -recipe_id (String): The recipe_id to check.
    #   -return_ingredient_names (Boolean) [Default: True]: If False, the ingredient IDs will be returned instead of the names.
    #Returns: List (Ingredient names or ingredient IDs)
    database = None
    cursor = None
    ingredients = []
    try:
        database = mysql.connector.connect(**mysql_info)
        cursor = database.cursor()
        if return_ingredient_names is True:
            cursor.execute("SELECT ingredient_name FROM table_ingredients WHERE ingredient_id IN (SELECT table_ingredients.ingredient_id FROM table_ingredients INNER JOIN link_recipe_ingredient ON table_ingredients.ingredient_id=link_recipe_ingredient.ingredient_id WHERE link_recipe_ingredient.recipe_id = %s)", (recipe_id,))
        else:
            cursor.execute("SELECT table_ingredients.ingredient_id FROM table_ingredients INNER JOIN link_recipe_ingredient ON table_ingredients.ingredient_id=link_recipe_ingredient.ingredient_id WHERE link_recipe_ingredient.recipe_id = %s", (recipe_id,))
        fetch = cursor.fetchall()
        cursor.close()
        database.close()
        if len(fetch) > 0:
            for ingredient in fetch:
                ingredients.append(ingredient[0])
        return ingredients
    except:
        if cursor is not None:
            cursor.close()
        if database is not None:
            database.close()
        return None

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
        return False
    
def link_add_recipe_ingredient(recipe_id, ingredient_id, auto_approve=False, database=None, cursor=None, close_connection=True):
    #Links a recipe to an ingredient and links the link to a user. A link must be approved by a moderator or an admin. Auto approve does this automatically.
    #Arguments:
    #   -recipe_id: The recipe to link the ingredient to.
    #   -ingredient_id: The ingredient to link the recipe to.
    #   -user_id: The user to link this link to.
    #   -auto_approve (Bool) [Default: False]: If True, any recipes will be automatically approved and assigned the approver of SYSTEM. 
    #   -database (None or database object) [Defaul: None]: The database connection to use. If None, a new connection is created.
    #   -cursor (None or database cursor object) [Default: None]: The cursor to use to interact with the database. If None or if the database is None, a new one is created.
    #   -close_connection (Bool) [Default: True]: If True, the database connection (and the cursor) will be closed. If False, they will be left open.
    #Returns: Boolean (True: Recipe was linked to user succesfully, False: Recipe failed to be linked; an error occurred)
    try:
        if database is None or cursor is None:
            database = mysql.connector.connect(**mysql_info)
            cursor = database.cursor()
        cursor.execute("INSERT INTO link_recipe_ingredient(recipe_id, ingredient_id, user_id, link_date) VALUES(%s, %s, %s, %s)", (recipe_id, ingredient_id, SYSTEM_USER_ID, get_time(database_time=True)),)
        #Line 115 is causing an error?
        database.commit()
        if auto_approve is True:
            cursor.execute("UPDATE link_recipe_ingredient SET link_isApproved = 1, approve_date = %s, approve_user_id = %s WHERE recipe_id = %s AND ingredient_id = %s", (get_time(database_time=True), SYSTEM_USER_ID, recipe_id, ingredient_id))
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

def link_add_recipe_dietary(recipe_id, dietary_id, auto_approve=False, database=None, cursor=None, close_connection=True):
    #Links a recipe to the specified dietary info and links the link to a user. A link must be approved by a moderator or an admin. Auto approve does this automatically.
    #Arguments:
    #   -recipe_id: The recipe to link the ingredient to.
    #   -dietary_id: The dietary info to link the recipe to.
    #   -user_id: The user to link this link to.
    #   -auto_approve (Bool) [Default: False]: If True, any recipes will be automatically approved and assigned the approver of SYSTEM. 
    #   -database (None or database object) [Defaul: None]: The database connection to use. If None, a new connection is created.
    #   -cursor (None or database cursor object) [Default: None]: The cursor to use to interact with the database. If None or if the database is None, a new one is created.
    #   -close_connection (Bool) [Default: True]: If True, the database connection (and the cursor) will be closed. If False, they will be left open.
    #Returns: Boolean (True: Recipe was linked to user succesfully, False: Recipe failed to be linked; an error occurred)
    try:
        if database is None or cursor is None:
            database = mysql.connector.connect(**mysql_info)
            cursor = database.cursor()
        cursor.execute("INSERT INTO link_recipe_dietary(recipe_id, dietary_id, user_id, link_date) VALUES(%s, %s, %s, %s)", (recipe_id, dietary_id, SYSTEM_USER_ID, get_time(database_time=True)),)
        database.commit()
        if auto_approve is True:
            cursor.execute("UPDATE link_recipe_dietary SET link_isApproved = 1, approve_date = %s, approve_user_id = %s WHERE recipe_id = %s AND dietary_id = %s", (get_time(database_time=True), SYSTEM_USER_ID, recipe_id, dietary_id))
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
    
'''Ingredients'''
#Check
def link_check_ingredient_user(ingredient_id, database=None, cursor=None, close_connection=True):
    #Checks if the specified ingredient is linked to a user or not.
    #Arguments:
    #   -ingredient_id: The ingredient to check.
    #   -database (None or database object) [Defaul: None]: The database connection to use. If None, a new connection is created.
    #   -cursor (None or database cursor object) [Default: None]: The cursor to use to interact with the database. If None or if the database is None, a new one is created.
    #   -close_connection (Bool) [Default: True]: If True, the database connection (and the cursor) will be closed. If False, they will be left open.
    #Returns: Boolean (True: The recipe is linked to a user, False: The recipe is not linked to a user; an error occurred)
    try:
        if database is None or cursor is None:
            database = mysql.connector.connect(**mysql_info)
            cursor = database.cursor()
        cursor.execute("SELECT ingredient_id FROM link_ingredient_user WHERE ingredient_id = %s", (str(ingredient_id),))
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
def link_add_ingredient_user(ingredient_id, user_id, auto_approve=False, database=None, cursor=None, close_connection=True):
    #Links a recipe to a user. The linked user is then considered to be the user that originally added it. A link must be approved by a moderator or an admin. Auto approve does this automatically.
    #Arguments:
    #   -ingredient_id: The ingredient to link the user to.
    #   -user_id: The user to link to the ingredient.
    #   -auto_approve (Bool) [Default: False]: If True, any recipes will be automatically approved and assigned the approver of SYSTEM. 
    #   -database (None or database object) [Defaul: None]: The database connection to use. If None, a new connection is created.
    #   -cursor (None or database cursor object) [Default: None]: The cursor to use to interact with the database. If None or if the database is None, a new one is created.
    #   -close_connection (Bool) [Default: True]: If True, the database connection (and the cursor) will be closed. If False, they will be left open.
    #Returns: Boolean (True: Ingredient was linked to user succesfully, False: Ingredient failed to be linked; an error occurred)
    try:
        if database is None or cursor is None:
            database = mysql.connector.connect(**mysql_info)
            cursor = database.cursor()
        cursor.execute("INSERT INTO link_ingredient_user(ingredient_id, user_id, link_date) VALUES(%s, %s, %s)", (ingredient_id, user_id, get_time(database_time=True)),)
        database.commit()
        if auto_approve is True:
            cursor.execute("UPDATE link_ingredient_user SET link_isApproved = 1, approve_date = %s, approve_user_id = %s WHERE ingredient_id = %s AND user_id = %s", (get_time(database_time=True), SYSTEM_USER_ID, ingredient_id, user_id))
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
    
'''Dietary Info'''
#Check
def link_check_dietary_user(dietary_id, database=None, cursor=None, close_connection=True):
    #Checks if the specified dietary info is linked to a user or not.
    #Arguments:
    #   -dietary_id: The dietary info to check.
    #   -database (None or database object) [Defaul: None]: The database connection to use. If None, a new connection is created.
    #   -cursor (None or database cursor object) [Default: None]: The cursor to use to interact with the database. If None or if the database is None, a new one is created.
    #   -close_connection (Bool) [Default: True]: If True, the database connection (and the cursor) will be closed. If False, they will be left open.
    #Returns: Boolean (True: The dietary info is linked to a user, False: The dietary info is not linked to a user; an error occurred)
    try:
        if database is None or cursor is None:
            database = mysql.connector.connect(**mysql_info)
            cursor = database.cursor()
        cursor.execute("SELECT dietary_id FROM link_dietary_user WHERE dietary_id = %s", (str(dietary_id),))
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
def link_add_dietary_user(dietary_id, user_id, auto_approve=False, database=None, cursor=None, close_connection=True):
    #Links the dietary info to a user. The linked user is then considered to be the user that originally added it. A link must be approved by a moderator or an admin. Auto approve does this automatically.
    #Arguments:
    #   -dietary_id: The dietary info to link the user to.
    #   -user_id: The user to link to the ingredient.
    #   -auto_approve (Bool) [Default: False]: If True, any recipes will be automatically approved and assigned the approver of SYSTEM. 
    #   -database (None or database object) [Defaul: None]: The database connection to use. If None, a new connection is created.
    #   -cursor (None or database cursor object) [Default: None]: The cursor to use to interact with the database. If None or if the database is None, a new one is created.
    #   -close_connection (Bool) [Default: True]: If True, the database connection (and the cursor) will be closed. If False, they will be left open.
    #Returns: Boolean (True: Dietary info was linked to user succesfully, False: Dietary info failed to be linked; an error occurred)
    try:
        if database is None or cursor is None:
            database = mysql.connector.connect(**mysql_info)
            cursor = database.cursor()
        cursor.execute("INSERT INTO link_dietary_user(dietary_id, user_id, link_date) VALUES(%s, %s, %s)", (dietary_id, user_id, get_time(database_time=True)),)
        database.commit()
        if auto_approve is True:
            cursor.execute("UPDATE link_dietary_user SET link_isApproved = 1, approve_date = %s, approve_user_id = %s WHERE dietary_id = %s AND user_id = %s", (get_time(database_time=True), SYSTEM_USER_ID, dietary_id, user_id))
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