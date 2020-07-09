from local.ManageAdditonalTask import ManageAdditionalTask


class Obj:

    def __init__(self, path, status):
        self.download_path = path
        self.status = status

    def get_download_status(self):
        return self.status


obj1 = Obj(path=r'C:\TEAMCITY_TEST\NABLER\F_Drive\Artifacts\AuditUI', status=True)
obj2 = Obj(path=r'C:\TEAMCITY_TEST\NABLER\F_Drive\Artifacts\SQL', status=True)

env_setting = {u'db_to_setup': {u'db_to_delete': [u'Vertex', u'VertexArch', u'GamesArch', u'Games', u'Misc'],
                                u'db_script': u'XSeries_and_Games_on_PC.sql', u'db_script_mod': {
        u'find_replace': {u'find_text': [u'VertexXYZ', u'GamesXYZ', u'MiscXYZ'],
                          u'replace_text': [u'Vertex', u'Games', u'Misc'], u'mod': u'no'},
        u'db_size': {u'new_size': u'40MB', u'original_size': u'10240MB', u'mod': u'yes'}}},
               u'windows_process_to_stop': [u'Aristocrat.Watchdog.Service.exe', u'VertexShell.exe',
                                            u'Aristocrat.Vertex.Service.exe', u'Aristocrat.Cms.ServiceHost.exe',
                                            u'Aristocrat.InterfaceBoard.ServiceHost.exe', u'ValyriaTray.exe'],
               u'artifact_config_folder': u'Configurations', u'exclude_file_extension': [u'.pdb'],
               u'download_artifact_root_path': u'C:\\TEAMCITY_TEST\\NABLER\\F_Drive\\Artifacts',
               u'sql_scripts_run': "configuration/Backup_VertexDB_RAMClear.sql"}

application_details = {
    u'AuditUI': {u'copy_config_to_path': None, u'tags': None, u'config_file_name': None, u'folder_name': u'AuditUI',
                 u'copy_artifacts_to_path': [u'C:\\TEAMCITY_TEST\\NABLER\\D_Drive\\AuditUI'], 'Download': obj1,
                 u'buildTypeID': u'Vertex_AuditUI_AuditUITrunk', u'anchor': u'AuditUI_Publish'},
    u'SQL': {u'copy_config_to_path': None,
             u'tags': None,
             u'config_file_name': None,
             u'folder_name': u'SQL',
             u'copy_artifacts_to_path': None,
             'Download'
             : obj2, u'buildTypeID': u'Vertex_VertexNext', u'anchor': u'SQL'}}

manage_test = ManageAdditionalTask(application_details=application_details, environment_setting=env_setting,
                                   database_connection='test')

print manage_test.__get_back_sql_script_path()
