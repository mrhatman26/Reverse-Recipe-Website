import sys, mysql.connector, csv, ast
from global_vars import mysql_info
from file_paths import SCRAPED_FILE_DIR
from misc import set_database_config
from db_handler_general import recipe_add_new
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
    print("Adding recipes to database...", end="", flush=True)
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
        recipe_add_new(recipe_info, auto_approve=True, database=database, cursor=cursor, close_connection=False)
        print("Adding recipes to database..." + str(recipe_no + 1) + "/" + recipe_count, end="\r", flush=True)
        recipe_no += 1
    print("Adding recipes to database...Done.")

def add_ingredients():
    print("Adding ingredients to database and linking to recipes...", end="", flush=True)
    ingredient_info = {}
    for recipe in recipe_data:
        for ingredient in ast.literal_eval(recipe[7]):
            eeee

#Main
access_log("localhost", "SYSTEM", "load_csv_data.py", admin=True)
set_database_config(sys.argv)
database = mysql.connector.connect(**mysql_info)
cursor = database.cursor()
load_recipe_data()
add_recipes()
cursor.close()
database.close()