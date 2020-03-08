from framework_config import local_database_setting
from local.database import Database
from util import file_actions as File


def delete_exisiting_database(database, db_to_delete):
    for item in db_to_delete:
        status = database.delete_db(item)
        # status = database_object.db_exists(item)
        print "{0} delete status: {1} ".format(item, status)

def setup_sql_script(sql_path):
    File.file_exists(sql_path)
    try:
        if 'Vertex_and_Games_on_PC.sql' in sql_path and local_database_setting["db_size"]["reduce"].lower() == 'yes':
            FIND_TEXT = ['VertexXYZ', 'GamesXYZ', 'MiscXYZ', '10240MB']
            REPLACE_TEXT = ['Vertex', 'Games', 'Misc', local_database_setting["db_size"]["new_size"]]
            File.find_replace_text_many(sql_path, FIND_TEXT, REPLACE_TEXT)
        elif local_database_setting["db_size"]["reduce"].lower() == 'yes':
            File.find_replace_text(sql_path, '10240MB',  local_database_setting["db_size"]["new_size"])
    except KeyError as err:
        print "Key error: {0}\nLists: {1}".format(err.message, err.args)
    except NameError as err:
            print "Name error: {0}\nLists: {1}".format(err.message, err.args)


def recreate_database_from_script(sql_path):
    vertex_database = Database()
    try:
        delete_exisiting_database(vertex_database, db_to_delete=local_database_setting["db_to_delete"])
    except KeyError as err:
        print "Key error: {0}\nLists: {1}".format(err.message, err.args)
    except NameError as err:
            print "Name error: {0}\nLists: {1}".format(err.message, err.args)

    setup_sql_script(sql_path)

    vertex_database.execute_sql_script(sql_script_path=sql_path)

