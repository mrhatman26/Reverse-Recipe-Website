import sys, mysql.connector, csv, ast, os, time
from global_vars import mysql_info
from file_paths import SCRAPED_FILE_DIR
from misc import set_database_config
from db_handler_general import recipe_add_new, recipe_check_name_exists, recipe_get_id, ingredient_add_new, ingredient_check_name_exists, ingredient_get_id, dietary_add_new, dietary_get_id, dietary_check_name_exists
from db_handler_links import link_add_recipe_ingredient, link_check_recipe_ingredient, link_check_recipe_dietary, link_add_recipe_dietary
from action_logger import access_log

recipe_data = []
headers = []
database = None
cursor = None

#Funcs
def load_recipe_data():
    global recipe_data, headers
    print("Loading data from " + SCRAPED_FILE_DIR + "...", end="", flush=True)
    with open(SCRAPED_FILE_DIR, "r", encoding="utf-8-sig") as csvfile:
        reader = csv.reader(csvfile)
        recipe_dict = {}
        for recipe in reader:
            recipe_data.append(recipe)
        headers = recipe_data.pop(0)
    print("Done.")

def add_recipes():
    recipe_count = str(len(recipe_data))
    recipe_info = {}
    recipe_no = 0
    for recipe in recipe_data:
        recipe_info = {
            "recipe_name": recipe[1],
            "recipe_author": recipe[2],
            "recipe_prep": recipe[3],
            "recipe_cook_time": recipe[4],
            "recipe_serve_size": recipe[5],
            "recipe_method": recipe[9],
            "recipe_type": recipe[10],
            "recipe_scraped": 1,
            "recipe_source_url": recipe[11],
            "recipe_isDeleted": 0
        }
        if recipe_check_name_exists(recipe_info["recipe_name"], database=database, cursor=cursor, close_connection=False) is False:
            recipe_add_new(recipe_info, auto_approve=True, database=database, cursor=cursor, close_connection=False)
        print("Adding recipes to database..." + str(recipe_no + 1) + "/" + recipe_count, end="\r", flush=True)
        recipe_no += 1
    print("Adding recipes to database...Done.", flush=True)

def add_ingredients():
    ingredient_info = {}
    recipe_count = str(len(recipe_data))
    recipe_no = 0
    for recipe in recipe_data:
        recipe[7] = str(recipe[7])
        try:
            if recipe[7].isspace() is False and recipe[7] != "":
                for ingredient in ast.literal_eval(recipe[7]):
                    ingredient_info = {
                        "ingredient_name": ingredient,
                        "ingredient_desc": None
                    }
                    if ingredient_check_name_exists(ingredient_info["ingredient_name"], database=database, cursor=cursor, close_connection=False) is False:
                        ingredient_add_new(ingredient_info, auto_approve=True, database=database, cursor=cursor, close_connection=False)
                    recipe_id = recipe_get_id(recipe[1], database=database, cursor=cursor, close_connection=False)
                    ingredient_id = ingredient_get_id(ingredient_info["ingredient_name"], database=database, cursor=cursor, close_connection=False)
                    if link_check_recipe_ingredient(recipe_id, ingredient_id, database=database, cursor=cursor, close_connection=False) is False:
                        link_add_recipe_ingredient(recipe_id, ingredient_id, auto_approve=True, database=database, cursor=cursor, close_connection=False)
            print("Adding ingredients to database from recipes..." + str(recipe_no + 1) + "/" + recipe_count, end="\r", flush=True)
        except:
            pass
        recipe_no += 1
    print("Adding ingredients to database from recipes...Done")

def add_dietary_info():
    dietary_info = {}
    recipe_count = str(len(recipe_data))
    recipe_no = 0
    for recipe in recipe_data:
        dietary_data = str(recipe[6])
        try:
            if dietary_data.isspace() is False and dietary_data != "":
                for dietary_item in ast.literal_eval(dietary_data):
                    dietary_info = {
                        "dietary_name": dietary_item,
                        "dietary_desc": None
                    }
                #Check if dietary info exists. If it doesn't add it.
                if dietary_check_name_exists(dietary_info["dietary_name"], database=database, cursor=cursor, close_connection=False) is False:
                    dietary_add_new(dietary_info, auto_approve=True, database=database, cursor=cursor, close_connection=False)
                recipe_id = recipe_get_id(recipe[1], database=database, cursor=cursor, close_connection=False)
                dietary_id = dietary_get_id(dietary_info["dietary_name"], database=database, cursor=cursor, close_connection=False)
                if link_check_recipe_dietary(recipe_id, dietary_id, database=database, cursor=cursor, close_connection=False) is False:
                    link_add_recipe_dietary(recipe_id, dietary_id, auto_approve=True, database=database, cursor=cursor, close_connection=False)
                #Get recipe ID and dietary info ID.
                #Check if dietary info is linked to recipe, if not, link it.
            print("Adding dietary info to database from recipes..." + str(recipe_no + 1) + "/" + recipe_count, end="\r", flush=True)
        except:
            pass
        recipe_no += 1

def convert_time(time):
    time = round(time)
    hours = 0
    minutes = 0
    seconds = 0
    while True:
        if time >= 3600: #An hour
            time -= 3600
            hours += 1
        elif time >= 60: #A minute
            time -= 60
            minutes += 1
        elif time >= 1: #A second
            time -= 1
            seconds += 1
        else:
            break
    return [hours, minutes, seconds]

#Main
os.system("cls")
start_time = time.time()
access_log("localhost", "SYSTEM", "load_csv_data.py", admin=True)
set_database_config(sys.argv)
database = mysql.connector.connect(**mysql_info)
cursor = database.cursor()
load_recipe_data()
add_recipes()
add_ingredients()
add_dietary_info()
cursor.close()
database.close()
try:
    actual_final_time = time.time() - start_time
    final_time = convert_time(actual_final_time)
    time_file = open("..\load_csv_time.txt", "w")
    time_file.write("Loading CSV file into database took " + str(time.time() - start_time) + " seconds")
    time_file.write("\n(" + str(final_time[0]) + " hours, " + str(final_time[1]) + " minutes and " + str(final_time[2]) + " seconds)")
    time_file.close()
except:
    print("Failed to save program time")