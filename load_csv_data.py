import sys, mysql.connector, csv, ast, os
from global_vars import mysql_info
from file_paths import SCRAPED_FILE_DIR
from misc import set_database_config
from db_handler_general import recipe_add_new, recipe_check_name_exists, recipe_get_id, ingredient_add_new, ingredient_check_name_exists, ingredient_get_id
from db_handler_links import link_add_recipe_ingredient, link_check_recipe_ingredient
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
    import traceback
    from misc import pause
    for recipe in recipe_data:
        recipe[7] = str(recipe[7])
        try:
            if recipe[7].isspace() is False and recipe[7] != "":
                for ingredient in ast.literal_eval(recipe[7]):
                    ingredient_info = {
                        "ingredient_name": ingredient,
                        "ingredient_desc": None
                    }
                    if ingredient_check_name_exists(ingredient_info["ingredient_name"]) is False:
                        ingredient_add_new(ingredient_info, auto_approve=True, database=database, cursor=cursor, close_connection=False)
                    recipe_id = recipe_get_id(recipe[1], database=database, cursor=cursor, close_connection=False)
                    ingredient_id = ingredient_get_id(ingredient_info["ingredient_name"], database=database, cursor=cursor, close_connection=False)
                    if link_check_recipe_ingredient(recipe_id, ingredient_id, database=database, cursor=cursor, close_connection=False) is False:
                        link_add_recipe_ingredient(recipe_id, ingredient_id, auto_approve=True, database=database, cursor=cursor, close_connection=False)
            print("Adding ingredients to database from recipes..." + str(recipe_no + 1) + "/" + recipe_count, end="\r", flush=True)
        except:
            print(traceback.format_exc(), flush=True)
            print("'" + str(recipe[7]) + "'", flush=True)
            pause()
        recipe_no += 1
    print("Adding ingredients to database from recipes...Done")


#Main
os.system("cls")
access_log("localhost", "SYSTEM", "load_csv_data.py", admin=True)
set_database_config(sys.argv)
database = mysql.connector.connect(**mysql_info)
cursor = database.cursor()
load_recipe_data()
add_recipes()
add_ingredients()
cursor.close()
database.close()