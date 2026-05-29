DROP DATABASE IF EXISTS recipeDB;
CREATE DATABASE recipeDB;
USE recipeDB;

/*Regular Tables*/
/*Users Table*/
DROP TABLE IF EXISTS table_users;
CREATE TABLE table_users(
    user_id INT NOT NULL AUTO_INCREMENT,
    user_name TEXT NOT NULL,
    user_pass TEXT NOT NULL,
    user_email TEXT,
    user_isAdmin BOOLEAN NOT NULL DEFAULT 0,
    user_isMod BOOLEAN NOT NULL DEFAULT 0,
    user_isDeleted BOOLEAN NOT NULL DEFAULT 0,
    PRIMARY KEY(user_id)
);

/*Recipes Table*/
DROP TABLE IF EXISTS table_recipes;
CREATE TABLE table_recipes(
    recipe_id INT NOT NULL AUTO_INCREMENT,
    recipe_name TEXT NOT NULL,
    recipe_author TEXT,
    recipe_prep TEXT,
    recipe_cook_time TEXT,
    recipe_serve_size TEXT,
    recipe_method TEXT,
    recipe_type TEXT,
    recipe_image_name TEXT,
    recipe_scraped BOOLEAN NOT NULL DEFAULT 0,
    recipe_source_url TEXT,
    recipe_isDeleted BOOLEAN NOT NULL DEFAULT 0,
    PRIMARY KEY(recipe_id)
);

/*Ingredients Table*/
DROP TABLE IF EXISTS table_ingredients;
CREATE TABLE table_ingredients(
    ingredient_id INT NOT NULL AUTO_INCREMENT,
    ingredient_name TEXT NOT NULL,
    ingredient_desc TEXT,
    ingredient_isDeleted BOOLEAN NOT NULL DEFAULT 0,
    PRIMARY KEY(ingredient_id)
);

/*Dietary Info Table*/
DROP TABLE IF EXISTS table_dietary_info;
CREATE TABLE table_dietary_info(
    dietary_id INT NOT NULL AUTO_INCREMENT,
    dietary_name TEXT NOT NULL,
    dietary_desc TEXT,
    dietary_isDeleted BOOLEAN NOT NULL DEFAULT 0,
    PRIMARY KEY(dietary_id)
);

/*Link Tables*/
/*Link Recipe to User*/
DROP TABLE IF EXISTS link_recipe_user;
CREATE TABLE link_recipe_user(
    link_id INT NOT NULL AUTO_INCREMENT,
    recipe_id INT NOT NULL,
    user_id INT NOT NULL,
    link_date DATETIME NOT NULL,
    link_isApproved BOOLEAN NOT NULL DEFAULT 0,
    approve_date DATETIME,
    approve_user_id INT,
    approve_reason TEXT,
    PRIMARY KEY(link_id),
    FOREIGN KEY(recipe_id) REFERENCES table_recipes(recipe_id),
    FOREIGN KEY(user_id) REFERENCES table_users(user_id),
    FOREIGN KEY(approve_user_id) REFERENCES table_users(user_id)
);

/*Link Ingredient to User*/
DROP TABLE IF EXISTS link_ingredient_user;
CREATE TABLE link_ingredient_user(
    link_id INT NOT NULL AUTO_INCREMENT,
    ingredient_id INT NOT NULL,
    user_id INT NOT NULL,
    link_date DATETIME NOT NULL,
    link_isApproved BOOLEAN NOT NULL DEFAULT 0,
    approve_date DATETIME,
    approve_user_id INT,
    approve_reason TEXT,
    PRIMARY KEY(link_id),
    FOREIGN KEY(ingredient_id) REFERENCES table_ingredients(ingredient_id),
    FOREIGN KEY(user_id) REFERENCES table_users(user_id),
    FOREIGN KEY(approve_user_id) REFERENCES table_users(user_id)
);

/*Link Dietary Info to User*/
DROP TABLE IF EXISTS link_dietary_user;
CREATE TABLE link_dietary_user(
    link_id INT NOT NULL AUTO_INCREMENT,
    dietary_id INT NOT NULL,
    user_id INT NOT NULL,
    link_date DATETIME NOT NULL,
    link_isApproved BOOLEAN NOT NULL DEFAULT 0,
    approve_date DATETIME,
    approve_user_id INT,
    approve_reason TEXT,
    PRIMARY KEY(link_id),
    FOREIGN KEY(dietary_id) REFERENCES table_dietary_info(dietary_id),
    FOREIGN KEY(user_id) REFERENCES table_users(user_id),
    FOREIGN KEY(approve_user_id) REFERENCES table_users(user_id)
);

/*Link Recipe to Ingredient*/
DROP TABLE IF EXISTS link_recipe_ingredient;
CREATE TABLE link_recipe_ingredient(
    link_id INT NOT NULL AUTO_INCREMENT,
    recipe_id INT NOT NULL,
    ingredient_id INT NOT NULL,
    user_id INT NOT NULL,
    link_date DATETIME NOT NULL,
    link_isApproved BOOLEAN NOT NULL DEFAULT 0,
    approve_date DATETIME,
    approve_user_id INT,
    approve_reason TEXT,
    PRIMARY KEY(link_id),
    FOREIGN KEY(ingredient_id) REFERENCES table_ingredients(ingredient_id),
    FOREIGN KEY(user_id) REFERENCES table_users(user_id),
    FOREIGN KEY(approve_user_id) REFERENCES table_users(user_id)
);

/*Link Recipe to Dietary Info*/
DROP TABLE IF EXISTS link_recipe_dietary;
CREATE TABLE link_recipe_dietary(
    link_id INT NOT NULL AUTO_INCREMENT,
    recipe_id INT NOT NULL,
    dietary_id INT NOT NULL,
    user_id INT NOT NULL,
    link_date DATETIME NOT NULL,
    link_isApproved BOOLEAN NOT NULL DEFAULT 0,
    approve_date DATETIME,
    approve_user_id INT,
    approve_reason TEXT,
    PRIMARY KEY(link_id),
    FOREIGN KEY(recipe_id) REFERENCES table_recipes(recipe_id),
    FOREIGN KEY(dietary_id) REFERENCES table_dietary_info(dietary_id),
    FOREIGN KEY(user_id) REFERENCES table_users(user_id),
    FOREIGN KEY(approve_user_id) REFERENCES table_users(user_id)
);

/*The following entries are for linking tables to values that no longer exist*/
INSERT INTO table_users(user_id, user_name, user_pass, user_isAdmin, user_isMod) VALUES(-2, "SYSTEM", "NOPASS", 1, 1);
INSERT INTO table_users(user_id, user_name, user_pass, user_isDeleted) VALUES(-1, "DELETED", "NOPASS", 1);
INSERT INTO table_recipes(recipe_id, recipe_name, recipe_isDeleted) VALUES(-1, "DELETED", 1);
INSERT INTO table_ingredients(ingredient_id, ingredient_name, ingredient_isDeleted) VALUES(-1, "DELETED", 1);
INSERT INTO table_dietary_info(dietary_id, dietary_name, dietary_isDeleted) VALUES(-1, "DELETED", 1);