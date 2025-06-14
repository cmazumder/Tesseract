"""
Manage database task
"""

from os import system

import pyodbc


class Database:
    """
    Class to manage database connection and task
    Tasks: Connections, execution of sql script, query and getting results

    :param connection: database connection
    :type connection: pyodbc.Connection
    :param cursor: database cursor for operation
    :type cursor: pyodbc.Cursor
    :param sql_script_execute_string: SQL query string
    :type sql_script_execute_string: str

    """
    sql_script_execute_string = None

    def __init__(self, server, username, password):
        """ constructor"""
        try:
            self.sql_script_execute_string = r"call osql -S {0} -U {1} -P {2} -d master -n -i ".format(
                server, username, password)
            try:
                self.connection, self.cursor = self.connect_to_db(db_server=server,
                                                                  db_username=username,
                                                                  db_password=password)
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

        :param db_server: database service/instance name
        :type db_server: str
        :param db_username: database user name for authentication
        :type db_username: str
        :param db_password: database password for authentication
        :type db_password: str
        :return: connection, cursor
        :rtype: pyodbc.Connection, pyodbc.Cursor
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
        Send SQL Query to database for execution and return status

        :param sql_query: SQL query
        :type sql_query: str
        :return: True/False
        :rtype: bool
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
        Send SQL Query to database for execution and return result

        :param sql_query: SQL query
        :type sql_query: str
        :return: self.cursor.fetchall()
        :rtype: list
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
        """
        Delete database with the database name

        :param database_name: name of database
        :type database_name: str
        :return: True/False
        :rtype: bool
        """
        if self.db_exists(database_name=database_name):
            if self.delete_backup_history(database_name=database_name):
                print "Deleted {} backup history".format(database_name)
                if self.set_single_user_mode(database_name=database_name):
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
        """
        Delete Database Backup and Restore history from MSDB System Database

        :param database_name: name of database
        :type database_name: str
        :return: SQL result
        :rtype: str
        """
        sql_statement = "EXEC msdb.dbo.sp_delete_database_backuphistory N'{}'".format(database_name)
        return self.execute_sql_query(sql_query=sql_statement)

    def set_single_user_mode(self, database_name):
        """
        Get exclusive access of database (before dropping)

        :param database_name: name of database
        :type database_name: str
        :return: SQL result
        :rtype: str
        """
        sql_statement = "ALTER DATABASE [{}] SET SINGLE_USER WITH ROLLBACK IMMEDIATE".format(database_name)
        return self.execute_sql_query(sql_query=sql_statement)

    def drop_db(self, database_name):
        """
        Drop database in SQL Server

        :param database_name: name of database
        :type database_name: str
        :return: SQL result
        :rtype: str
        """
        sql_statement = "DROP DATABASE [{}]".format(database_name)
        return self.execute_sql_query(sql_query=sql_statement)

    def db_exists(self, database_name):
        """
        Check if database is present

        :param database_name: name of database
        :type database_name: str
        :return: True/False
        :rtype: bool
        """
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
        """
        Execute SQL script from path

        :param sql_script_path: path to SQL script
        :type sql_script_path: str
        """
        batch_to_execute = self.sql_script_execute_string + "{}".format(sql_script_path)
        try:
            system(batch_to_execute)
        except Exception as E:
            print "Message: {}\nArgs {}".format(E.message, E.args)
