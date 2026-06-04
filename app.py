import ast, traceback, sys
from flask import Flask, render_template, url_for, request, redirect, abort
from flask_login import LoginManager, current_user, login_user, logout_user
from db_handler_users import *
from db_handler_general import *
from db_handler_admin import *
from db_handler_links import link_get_recipe_user_id, link_get_recipe_ingredients
from action_logger import *
from version_handler import *
from user import User
from global_vars import deployed, live
from misc import set_database_config, get_current_page
#ToDo: Investigate why a recipe page with an invalid ID still acts as though nothing is wrong.

'''Server Vars'''
version = update_version()
fprint("Version is now: " + str(version))
set_database_config(sys.argv)
app = Flask(__name__) #Create the flask application
app.secret_key = "SeeThatMountain?YouCanClimbItJERSAIKGYHJIOERHGJ"

'''Login Manager'''
login_manager = LoginManager()
login_manager.init_app(app)
@login_manager.user_loader
def load_fuser(id):
    user_check = user_check_reconfirm(id)
    if len(user_check) <= 0:
        return None
    else:
        return User(user_check[0], user_check[1], user_check[2], user_check[3])

def get_user():
    try:
        if hasattr(current_user, 'username'):
            return current_user.username
        else:
            return "Annonymous"
    except:
        return "Annonymous"

'''General Routes'''
#Home/Index
@app.route("/")
def home():
    access_log(request.remote_addr, get_user(), request.path)
    return render_template('home.html', page_name="Home", c_version=version)

'''Recipe Routes'''
#All Recipes
@app.route('/recipes/')
@app.route('/recipes/pid=<starting_id>')
@app.route('/recipes/pid=<starting_id>&search=<search>')
@app.route('/recipes/pid=<starting_id>&search=<search>&search_type=<search_type>')
def recipes_default(starting_id=0, search="", no_results=10, search_type=0):
    access_log(request.remote_addr, get_user(), request.path)
    starting_id = int(starting_id)
    recipes = recipe_get_all_partial(starting_id, search=search, search_type=search_type)
    current_page = get_current_page(starting_id, no_results)
    return render_template("recipes/recipe_list.html", page_name="All Recipes", c_version=version, recipe_list=recipes[0], no_pages=recipes[1], total_recipes=recipes[2], no_results=no_results, current_page=current_page + 1, starting_id=starting_id, search=search)

#Individual Recipes
@app.route('/recipes/recipe_id=<recipe_id>')
def recipes_individual(recipe_id=0):
    access_log(request.remote_addr, get_user(), request.path)
    recipe_info = recipe_get_individual_info(recipe_id)
    recipe_name = "Uknown Recipe"
    recipe_method = []
    if recipe_info is not None:
        recipe_info["recipe_user"] = user_get_username(link_get_recipe_user_id(recipe_id))
        recipe_info["recipe_ingredients"] = link_get_recipe_ingredients(recipe_id)
        if len(recipe_info) > 0:
            recipe_name = recipe_info["recipe_name"]
            recipe_method = ast.literal_eval(recipe_info["recipe_method"])
        else:
            recipe_info = None
    return render_template("recipes/recipe_individual.html", page_name=recipe_name, c_version=version, recipe_data=recipe_info, recipe_method=recipe_method)

'''Ingredient Routes'''
#All Ingredients
@app.route('/ingredients/')
@app.route('/ingredients/pid=<starting_id>')
@app.route('/ingredients/pid=<starting_id>&search=<search>')
def ingredients_list(starting_id=0, no_results=10, search=""):
    access_log(request.remote_addr, get_user(), request.path)
    try:
        starting_id = int(starting_id)
    except:
        starting_id = 0
    ingredients = ingredient_get_all(starting_id, no_results, search)
    current_page = get_current_page(starting_id, no_results)
    empty_search = True
    if search.isspace() is False and search != "":
        empty_search = False
    return render_template("ingredients/ingredient_list.html", page_name="All Ingredients", c_version=version, ingredient_search=search, empty_search=empty_search, ingredient_list=ingredients[0], no_pages=ingredients[1], total_ingredients=ingredients[2], no_results=no_results, current_page=current_page + 1, starting_id=starting_id, search=search)

#Individual Ingredient
@app.route('/ingredients/ingredient_id=<ingredient_id>')
def ingredient_individual(ingredient_id=0):
    access_log(request.remote_addr, get_user(), request.path)
    ingredient_info = ingredient_get_info(ingredient_id)
    ingredient_name = "Uknown Ingredient"
    if len(ingredient_info) > 0:
        ingredient_name = ingredient_info["ingredient_name"]
        if ingredient_info["ingredient_desc"] == "" or ingredient_info["ingredient_desc"].isspace() is True:
            ingredient_info["ingredient_desc"] = None
    fprint(ingredient_info)
    return render_template("ingredients/ingredient_individual.html", page_name=ingredient_name, c_version=version, ingredient_data=ingredient_info)

'''User Routes'''
#Account Page
@app.route("/users/account/")
def user_account():
    if current_user.is_authenticated:
        access_log(request.remote_addr, get_user(), request.path)
        user_data = user_single_get_all(current_user.id)
        return render_template("users/user_page.html", page_name=get_user(), user_data=user_data, c_version=version)
    else:
        access_log(request.remote_addr, get_user(), request.path, failed=True, no_auth=True)
        return redirect("/users/login/")

#Login
@app.route("/users/login/")
def user_login():
    if current_user.is_authenticated:
        access_log(request.remote_addr, get_user(), request.path, failed=True)
        return redirect("/")
    else:
        access_log(request.remote_addr, get_user(), request.path)
        return render_template("users/login.html", page_name="Login", c_version=version)
@app.route("/users/login/validate/", methods=["POST"])
def user_login_validate():
    if current_user.is_authenticated:
        access_log(request.remote_addr, get_user(), request.path, failed=True)
        return redirect("/")
    else:
        userdata = request.get_data()
        userdata = userdata.decode()
        try:
            userdata = ast.literal_eval(userdata)
            if user_check_exists(userdata["user_name"]):
                if user_login_passcheck(userdata):
                    admin_stat = user_check_admin(userdata["user_name"])
                    login_user(User(user_get_id(userdata["user_name"]), userdata["user_name"], admin_stat[0], admin_stat[1]))
                    login_log(request.remote_addr, userdata["user_name"])
                    return "success"
                else:
                    login_log(request.remote_addr, userdata["user_name"], failed=True)
                    error_log(request.remote_addr, userdata["user_name"], "user_login_validate failed to validate login")
                    return "usernotexist"
            else:
                login_log(request.remote_addr, userdata["user_name"], failed=True)
                error_log(request.remote_addr, userdata["user_name"], "User does not exist")
                return "usernotexist"
        except Exception as e:
            login_log(request.remote_addr, userdata["user_name"], failed=True)
            error_log(request.remote_addr, userdata["user_name"], "Server error during login", theException=traceback.format_exc())
            return "servererror"

#Signup
@app.route("/users/signup/")
def user_signup():
    if current_user.is_authenticated:
        access_log(request.remote_addr, get_user(), request.path, failed=True)
        return redirect("/")
    else:
        access_log(request.remote_addr, get_user(), request.path)
        return render_template("users/signup.html", page_name="Signup", c_version=version)
@app.route("/users/signup/validate/", methods=["POST"])
def user_signup_validate():
    if current_user.is_authenticated:
        access_log(request.remote_addr, get_user(), request.path, failed=True)
        return redirect("/")
    else:
        access_log(request.remote_addr, get_user(), request.path)
        userdata = request.get_data()
        userdata = userdata.decode()
        userdata = ast.literal_eval(userdata)
        try:
            if user_check_exists(userdata["user_name"]) is False:
                if user_add_new(userdata) is True:
                    new_user_log(request.remote_addr, userdata["user_name"])
                    return "success"
                else:
                    new_user_log(request.remote_addr, userdata["user_name"], failed=True)
                    error_log(request.remote_addr, userdata["user_name"], "user_add_new failed to create a new user")
                    return "servererror"
            else:
                new_user_log(request.remote_addr, userdata["user_name"], failed=True)
                error_log(request.remote_addr, userdata["user_name"], "User already exists")
                return "userexists"
        except Exception as e:
            new_user_log(request.remote_addr, userdata["user_name"], failed=True)
            error_log(request.remote_addr, userdata["user_name"], "Server error during user creation", theException=traceback.format_exc())
            return "servererror"
        
#Update Username
@app.route("/users/modify/username/", methods=["POST"])
def user_change_username():
    if current_user.is_authenticated:
        access_log(request.remote_addr, get_user(), request.path)
        new_username = request.get_data()
        new_username = new_username.decode()
        new_username = ast.literal_eval(new_username)
        if current_user.username != new_username["user_name"]:
            if user_check_exists(new_username["user_name"]) is False:
                old_username = get_user()
                if user_modify_username(current_user.id, new_username["user_name"]) is True:
                    modify_user_log(request.remote_addr, old_username, new_username["user_name"], is_username=True)
                    return "success"
                else:
                    modify_user_log(request.remote_addr, get_user(), new_username["user_name"], is_username=True, failed=True)
                    return "servererror"
            else:
                modify_user_log(request.remote_addr, get_user(), new_username["user_name"], is_username=True, failed=True)
                return "userexists"
        else:
            modify_user_log(request.remote_addr, get_user(), new_username["user_name"], is_username=True, failed=True)
            return "samename"
    else:
        return "servererror"
    
#Update Email
@app.route("/users/modify/email/", methods=["POST"])
def user_change_email():
    if current_user.is_authenticated:
        access_log(request.remote_addr, get_user(), request.path)
        new_email = request.get_data()
        new_email = new_email.decode()
        new_email = ast.literal_eval(new_email)
        old_email = user_get_email(current_user.id)
        if old_email != new_email["user_email"]:
            if user_modify_email(current_user.id, new_email["user_email"]) is True:
                modify_user_log(request.remote_addr, get_user(), new_email["user_email"], is_email=True)
                return "success"
            else:
                modify_user_log(request.remote_addr, get_user(), new_email["user_email"], is_email=True, failed=True)
                return "servererror"
        else:
            modify_user_log(request.remote_addr, get_user(), new_email["user_email"], is_email=True, failed=True)
            return "sameemail"
    else:
        return "servererror"

#Delete Account    
@app.route("/users/modify/delete/")
def user_delete_validate():
    if current_user.is_authenticated:
        access_log(request.remote_addr, get_user(), request.path)
        return render_template("confirmation.html", page_name="Are you sure?", message="Are you sure you want to delete your account?", dir_to_use="user_delete_confirmed", dir_to_return="user_account", yes_message="Yes, DELETE my account", no_message="No, return to my account page", c_version=version)
    else:
        access_log(request.remote_addr, get_user(), request.path, failed=True, no_auth=True)
        abort(404)
@app.route("/users/modify/delete/confirmed/")
def user_delete_confirmed():
    if current_user.is_authenticated:
        access_log(request.remote_addr, get_user(), request.path)
        old_user = get_user()
        if user_delete(current_user.id) is True:
            logout_user()
            delete_user_log(request.remote_addr, old_user)
            login_log(request.remote_addr, old_user, logout=True, auto=True)
            return redirect("/")
        else:
            delete_user_log(request.remote_addr, old_user, failed=True)
            abort(500)
    else:
        access_log(request.remote_addr, get_user(), request.path, failed=True, no_auth=True)
        abort(404)
        
#Logout
@app.route("/users/logout/")
def user_logout():
    if current_user.is_authenticated:
        access_log(request.remote_addr, get_user(), request.path)
        login_log(request.remote_addr, get_user(), logout=True)
        logout_user()
        return redirect("/")
    else:
        access_log(request.remote_addr, get_user(), request.path, failed=True)
        return redirect("/")
    
'''Mod Routes'''
#Main
@app.route("/mod/")
def mod_main():
    if current_user.is_authenticated:
        if current_user.is_mod:
            access_log(request.remote_addr, get_user(), request.path)
            return render_template("mod/mod_main.html", page_name="Mod: Main", c_version=version)
        else:
            access_log(request.remote_addr, get_user(), request.path, failed=True)
            abort(404)
    else:
        access_log(request.remote_addr, get_user(), request.path, failed=True)
        abort(404)
    
'''Admin Routes'''
#Main
@app.route("/admin/")
def admin_main():
    if current_user.is_authenticated:
        if current_user.is_admin:
            access_log(request.remote_addr, get_user(), request.path, admin=True)
            return render_template("admin/admin_main.html", page_name="Admin: Main", c_version=version)
        else:
            access_log(request.remote_addr, get_user(), request.path, failed=True, admin=True, no_auth=True)
            abort(404)
    else:
        access_log(request.remote_addr, get_user(), request.path, failed=True, admin=True, no_auth=True)
        abort(404)

#User Management
@app.route("/admin/management/users/")
def admin_user_management():
    if current_user.is_authenticated:
        if current_user.is_admin:
            access_log(request.remote_addr, get_user(), request.path, admin=True)
            return render_template("admin/admin_user_management.html", page_name="Admin: User Management", c_version=version, userdata=user_get_all())
        else:
            access_log(request.remote_addr, get_user(), request.path, failed=True, admin=True, no_auth=True)
            abort(404)
    else:
        access_log(request.remote_addr, get_user(), request.path, failed=True, admin=True, no_auth=True)
        abort(404)

#Database Management
@app.route("/admin/management/databasae/")
def admin_database_manage():
    if current_user.is_authenticated:
        if current_user.is_admin:
            access_log(request.remote_addr, get_user(), request.path, admin=True)
            return render_template("admin/admin_database_management.html", page_name="Admin: Database Management", c_version=version)
        else:
            access_log(request.remote_addr, get_user(), request.path, admin=True, failed=True, no_auth=True)
            abort(404)
    else:
        access_log(request.remote_addr, get_user(), request.path, admin=True, failed=True, no_auth=True)
        abort(404)

#Error Pages
#These pages are only shown when the website encounters an error.
#404 is page not found.
@app.errorhandler(404)
def page_invalid(e):
    return render_template('errors/404.html'), 404
@app.errorhandler(405)
def page_wrong_method(e):
    return render_template('errors/405.html'), 405
@app.errorhandler(500)
def page_server_error(e):
    return render_template('errors/500.html'), 500
#For simplicity, if the website encounters a 405 error, it will redirect and show as a 404 instead.

#Favicon
#Apparently supposed to be the icon used when a page is bookmarked.
#Even though this supresses the "favicon.ico" 404 error, it does not show this icon when bookmarked.
@app.route('/favicon.ico')
def favicon():
    return url_for("static", filename="favicon.ico")

#Launch Website
if __name__ == '__main__':
    if live is True:
        from waitress import serve
        serve(app, host="0.0.0.0", port=5000)
    else:
        app.run(host="0.0.0.0", port=5000, debug=True)