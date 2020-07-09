from ConfigManager.ManageJsonConfig import get_dict_value
from local.database import Database
from util import FileActions as File


class DatabaseSetup:

    @staticmethod
    def delete_existing_database(database_connection, env_setting):
        db_to_delete = get_dict_value(env_setting, ["db_to_setup", "db_to_delete"])  # type: list
        if db_to_delete and len(db_to_delete) > 0:
            for item in db_to_delete:
                status = database_connection.delete_db(item)
                # status = database_object.db_exists(item)
                print "{0} delete status: {1} ".format(item, status)

    @staticmethod
    def setup_sql_script(sql_path, env_setting):
        find_text = []
        replace_text = []
        if str(get_dict_value(env_setting, ["db_to_setup", "db_script_mod", "find_replace", "mod"])).lower() == 'yes':
            find_text = get_dict_value(env_setting, ["db_to_setup", "db_script_mod", "find_replace", "find_text"])
            replace_text = get_dict_value(env_setting, ["db_to_setup", "db_script_mod", "find_replace", "replace_text"])

        if str(get_dict_value(env_setting, ["db_to_setup", "db_script_mod", "db_size", "mod"])).lower() == 'yes':
            find_text.append(get_dict_value(env_setting, ["db_to_setup", "db_script_mod", "db_size", "original_size"]))
            replace_text.append(get_dict_value(env_setting, ["db_to_setup", "db_script_mod", "db_size", "new_size"]))
        if find_text and replace_text and len(find_text) == len(replace_text):
            # use encoding for ANSI https://docs.python.org/2/library/codecs.html#standard-encodings
            File.find_replace_text_many(file_path=sql_path, find_text_list=find_text, replace_text_list=replace_text,
                                        encoding='mbcs')

    @staticmethod
    def recreate_database_from_script(database_connection, sql_path, env_setting):
        DatabaseSetup.setup_sql_script(sql_path, env_setting)
        DatabaseSetup.delete_existing_database(database_connection=database_connection, env_setting=env_setting)
        DatabaseSetup.execute_sql_script(database_connection=database_connection, sql_path=sql_path)

    @staticmethod
    def execute_sql_script(database_connection, sql_path):
        database_connection.execute_sql_script(sql_script_path=sql_path)

    @staticmethod
    def get_database_connection(server, username, password):
        return Database(server, username, password)
