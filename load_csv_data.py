import sys, mysql.connector
from global_vars import mysql_info
from file_paths import scraped_file_dir
from misc import set_database_config

#Funcs

set_database_config(sys.argv)
