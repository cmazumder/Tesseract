from local.database import Database
from util import file_actions as File

# This has to converted to class


def delete_existing_database(database_connection, db_to_delete):
    for item in db_to_delete:
        status = database_connection.delete_db(item)
        # status = database_object.db_exists(item)
        print "{0} delete status: {1} ".format(item, status)


def setup_sql_script(sql_path, find_text="10240MB", replace_text="100MB"):
    File.file_exists(sql_path)
    try:
        if 'Vertex_and_Games_on_PC.sql' in sql_path:
            FIND_TEXT = ['VertexXYZ', 'GamesXYZ', 'MiscXYZ', '10240MB']
            REPLACE_TEXT = ['Vertex', 'Games', 'Misc', replace_text]
            File.find_replace_text_many(file_path=sql_path, find_text_list=FIND_TEXT, replace_text_list=REPLACE_TEXT)
        else:
            File.find_replace_text(file_path=sql_path, find_text=find_text, replace_text=replace_text)
    except KeyError as err:
        print "Key error: {0}\nLists: {1}".format(err.message, err.args)
    except NameError as err:
        print "Name error: {0}\nLists: {1}".format(err.message, err.args)


def recreate_database_from_script(database_connection, sql_path, delete_db):
    setup_sql_script(sql_path)
    delete_existing_database(database_connection=database_connection, db_to_delete=delete_db)
    database_connection.execute_sql_script(sql_script_path=sql_path)


def get_database_connection(server, username, password):
    return Database(server, username, password)
