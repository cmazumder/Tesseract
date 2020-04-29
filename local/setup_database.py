from local.database import Database
from util import file_actions as File


def delete_exisiting_database(database, db_to_delete):
    for item in db_to_delete:
        status = database.delete_db(item)
        # status = database_object.db_exists(item)
        print "{0} delete status: {1} ".format(item, status)


def setup_sql_script(sql_path, find_text="10240MB", replace_text=None):
    File.file_exists(sql_path)
    try:
        if 'Vertex_and_Games_on_PC.sql' in sql_path:
            FIND_TEXT = ['VertexXYZ', 'GamesXYZ', 'MiscXYZ', '10240MB']
            REPLACE_TEXT = ['Vertex', 'Games', 'Misc', replace_text]
            File.find_replace_text_many(file_path=sql_path, find_text=FIND_TEXT, replace_text=REPLACE_TEXT)
        else:
            File.find_replace_text(file_path=sql_path, find_text=find_text, replace_text=replace_text)
    except KeyError as err:
        print "Key error: {0}\nLists: {1}".format(err.message, err.args)
    except NameError as err:
        print "Name error: {0}\nLists: {1}".format(err.message, err.args)


def recreate_database_from_script(sql_path, server, username, password):
    database_connection = get_database_connection(server=server, username=username, password=password)
    setup_sql_script(sql_path)
    database_connection.execute_sql_script(sql_script_path=sql_path)


def get_database_connection(server, username, password):
    return Database(server, username, password)
