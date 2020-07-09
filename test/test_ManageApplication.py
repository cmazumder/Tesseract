from local.ManageApplicationReplace import ManageApplicationReplace


class Obj:

    def __init__(self, path, status):
        self.download_path = path
        self.status = status

    def get_download_status(self):
        return self.status


def test_replace():
    # This is test function for this class

    obj1 = Obj(path=r'C:\TEAMCITY_TEST\NABLER\F_Drive\Artifacts\AuditUI', status=True)
    obj2 = Obj(path=r'C:\TEAMCITY_TEST\NABLER\F_Drive\Artifacts\SQL', status=True)

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

    application_name_keys = [u'AuditUI', u'SQL']

    config_folder_path = u'C:\\TEAMCITY_TEST\\NABLER\\F_Drive\\Artifacts\\Configurations'

    download_application_root_path = u'C:\\TEAMCITY_TEST\\NABLER\\F_Drive\\Artifacts'

    env_setting = {u'db_to_setup': {u'db_to_delete': [u'Vertex', u'VertexArch', u'GamesArch', u'Games', u'Misc'],
                                    u'db_script': u'XSeries_and_Games_on_PC.sql', u'db_script_mod': {
            u'find_replace': {u'find_text': [u'VertexXYZ', u'GamesXYZ', u'MiscXYZ'],
                              u'replace_text': [u'Vertex', u'Games', u'Misc'], u'mod': u'no'},
            u'db_size': {u'new_size': u'40MB', u'original_size': u'10240MB', u'mod': u'yes'}}},
                   u'windows_process_to_stop': [u'Aristocrat.Watchdog.Service.exe', u'VertexShell.exe',
                                                u'Aristocrat.Vertex.Service.exe', u'Aristocrat.Cms.ServiceHost.exe',
                                                u'Aristocrat.InterfaceBoard.ServiceHost.exe', u'ValyriaTray.exe'],
                   u'artifact_config_folder': u'Configurations', u'exclude_file_extension': [u'.pdb'],
                   u'download_artifact_root_path': u'C:\\TEAMCITY_TEST\\NABLER\\F_Drive\\Artifacts'}

    exclude_file_extension = [u'.pdb']

    process_to_terminate = [u'Aristocrat.Watchdog.Service.exe', u'VertexShell.exe', u'Aristocrat.Vertex.Service.exe',
                            u'Aristocrat.Cms.ServiceHost.exe', u'Aristocrat.InterfaceBoard.ServiceHost.exe',
                            u'ValyriaTray.exe']

    spacer_char_hyphen = '-' * 50
    spacer_char_asterisk = '*' * 65

    artifact = ManageApplicationReplace(application_details=application_details, env_setting=env_setting)
    artifact.replace_application()


test_replace()
