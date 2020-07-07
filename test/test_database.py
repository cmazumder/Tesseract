from local.database import Database

def test_Database():
    # This is test function for this class
    db = Database(server="localhost\\SQLEXPRESS", username="sa", password="Password1")
    db_to_delete = ['Vertex', 'VertexArch', 'GamesArch', 'Games', 'Misc']

    # for item in db_to_delete:
    #     status = database_object.delete_db(item)
    #     # status = database_object.db_exists(item)
    #     print "{0} delete status: {1} ".format(item, status)
    #     # database_object.delete_db('Vertex')
    #     time.sleep(5)
    db.execute_sql_script(sql_script_path=r'C:\Test_TeamCity\SampleDownload\SQL\Vertex_and_Games_on_PC.sql')

# test_Database()