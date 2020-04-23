from os import system

import pyodbc
from config.framework_config import local_database_setting


class Database:
    sql_script_execute_string = None

    def __init__(self):
        """ constructor"""
        try:
            self.sql_script_execute_string = r"call osql -S {0} -U {1} -P {2} -d master -n -i ".format(
                local_database_setting["db_server"],
                local_database_setting["db_username"],
                local_database_setting["db_password"])
            try:
                self.connection, self.cursor = self.connect_to_db(db_server=local_database_setting["db_server"],
                                                                  db_username=local_database_setting["db_username"],
                                                                  db_password=local_database_setting["db_password"])
            except pyodbc.Error as err:
                print "Database connection error:{0}\nSQL state: {1}".format(err.message, err.args)
        except (KeyError, NameError) as err:
            print "Error database init: {0}\nLists: {1}".format(err.message, err.args)

    def __del__(self):
        """ destructor"""
        pass

    def connect_to_db(self, db_server, db_username, db_password):
        """
        Connect to SQL Server
        :params: db_server, db_username, db_password
        :return: connection, cursor
        """
        try:
            connection_string = r"DRIVER={{SQL Server}};SERVER={0}; database={1}; " \
                                r"trusted_connection=yes;UID={2};PWD={3}" \
                .format(db_server, 'master', db_username, db_password)

            connection = pyodbc.connect(connection_string, autocommit=True)
            return connection, connection.cursor()
        except (pyodbc.Error, pyodbc.OperationalError) as err:
            print "Cannot setup database connection: {0}" \
                  "\nCode: {1}\nReason:{2}".format(err.message, err.args[0], err.args[1])
        return None, None

    def execute_sql_query(self, sql_query):
        """
        Query database and fetch data
        :param sql_query: Sql text query
        :return: data
        """
        try:
            if self.cursor:
                self.cursor.execute(sql_query)
                self.connection.commit()
                return True
            else:
                print "Cannot execute sql query\nIssue with database connection:".format(self.connection)
        except pyodbc.Error as err:
            self.connection.rollback()
            print "Failed to execute SQL query: {0}\n Error: {1}".format(sql_query, err.message)
        return False

    def get_result_from_sql_query(self, sql_query):
        """
        Query database and fetch data
        :param sql_query: Sql text query
        :return: data
        """
        try:
            if self.cursor:
                self.cursor.execute(sql_query)
                return self.cursor.fetchall()
            else:
                print "Cannot execute sql query\nIssue with database connection:".format(self.connection)
        except pyodbc.Error as E:
            print "Problem getting result. SQL query: {0} \n Error: {1}".format(sql_query, E.args)
        return False

    def delete_db(self, database_name):
        if self.db_exists(database_name=database_name):
            if self.delete_backup_history(database_name=database_name):
                print "Deleted {} backup history".format(database_name)
                if self.set_single_user_mode(db_name=database_name):
                    print "Set single user mode {}".format(database_name)
                    if self.drop_db(database_name=database_name):
                        print "{} dropped".format(database_name)
                        return True
                    else:
                        print "Cannot drop {}".format(database_name)
                else:
                    print "Cannot set single user mode {}".format(database_name)
            else:
                print "Cannot deleted {} backup history".format(database_name)
        else:
            print "{} is not present, cannot delete".format(database_name)
        return False

    def delete_backup_history(self, database_name):
        # Delete Database Backup and Restore history from MSDB System Database
        sql_statement = "EXEC msdb.dbo.sp_delete_database_backuphistory N'{}'".format(database_name)
        return self.execute_sql_query(sql_query=sql_statement)

    def set_single_user_mode(self, db_name):
        # Get exclusive access of database (before dropping)
        sql_statement = "ALTER DATABASE [{}] SET SINGLE_USER WITH ROLLBACK IMMEDIATE".format(db_name)
        return self.execute_sql_query(sql_query=sql_statement)

    def drop_db(self, database_name):
        # Drop database in SQL Server
        sql_statement = "DROP DATABASE [{}]".format(database_name)
        return self.execute_sql_query(sql_query=sql_statement)

    def db_exists(self, database_name):
        try:
            if self.cursor:
                sql_statement = "SELECT DB_ID(N'{}')".format(database_name)
                self.cursor.execute(sql_statement)
                if self.cursor.fetchval():
                    return True
        except pyodbc.Error as E:
            print "Problem getting result\n Error: {0}".format(E.args)
        return False

    def execute_sql_script(self, sql_script_path):
        batch_to_execute = self.sql_script_execute_string + "{}".format(sql_script_path)
        try:
            system(batch_to_execute)
        except Exception as E:
            print "Message: {}\nArgs {}".format(E.message, E.args)


def test_Database():
    db = Database()
    db_to_delete = ['Vertex', 'VertexArch', 'GamesArch', 'Games', 'Misc']

    # for item in db_to_delete:
    #     status = database_object.delete_db(item)
    #     # status = database_object.db_exists(item)
    #     print "{0} delete status: {1} ".format(item, status)
    #     # database_object.delete_db('Vertex')
    #     time.sleep(5)
    db.execute_sql_script(sql_script_path=r'C:\Test_TeamCity\SampleDownload\SQL\Vertex_and_Games_on_PC.sql')

# test_Database()
