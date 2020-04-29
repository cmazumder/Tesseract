from config.framework_config import artifacts_to_download, teamcity_download_setting, deployment_env_paths, \
    local_database_setting

from website.api.application import Application


class Service(Application):

    def __init__(self):
        Application.__init__(self)
        try:
            self.build_id = self.get_successful_buildid(
                build_type_id=teamcity_download_setting["service"]["buildTypeID"])
            self.folder = artifacts_to_download["service"]["folder_name"]
        except KeyError as err:
            print "Key error: {0}\nLists: {1}".format(err.message, err.args)
        except NameError as err:
            print "Name error: {0}\nLists: {1}".format(err.message, err.args)

    def __del__(self):
        pass

    def set_vertex_sql_properties(self):
        try:
            anchor_text = teamcity_download_setting["sql"]["anchor"]
            self.set_file_download_path(save_artifact_dir=deployment_env_paths["path_download_root"])
            self.set_artifact_url(self.build_id, anchor_text)
        except KeyError as err:
            print "Key error: {0}\nLists: {1}".format(err.message, err.args)
        except NameError as err:
            print "Name error: {0}\nLists: {1}".format(err.message, err.args)

    def download_vertex_sql(self):
        session_response = self.teamcity_session.get_url_response(self.artifact_url_complete,
                                                                  self.teamcity_session.username,
                                                                  self.teamcity_session.password)
        if session_response.status_code == 200:
            api_response = self.get_json_response_as_dict(self.artifact_url_complete)
            self.create_filelist_from_api(artifact_list_from_api=api_response,
                                          filename_to_get=[local_database_setting["db_to_setup"]])
            if self.artifact_file_details:
                self.start_download()
        else:
            print "Error {} \n url {}".format(session_response, self.artifact_url_complete)

    def set_vertex_service_properties(self):
        try:
            anchor_text = teamcity_download_setting["service"]["anchor"]
            self.set_file_download_path(save_artifact_dir=self.folder)
            self.set_artifact_url(self.build_id, 'Applications', anchor_text)
        except KeyError as err:
            print "Key error: {0}\nLists: {1}".format(err.message, err.args)
        except NameError as err:
            print "Name error: {0}\nLists: {1}".format(err.message, err.args)

    def download_vertex_service(self):
        session_response = self.teamcity_session.get_url_response(self.artifact_url_complete,
                                                                  self.teamcity_session.username,
                                                                  self.teamcity_session.password
                                                                  )
        if session_response.status_code == 200:
            api_response = self.get_json_response_as_dict(self.artifact_url_complete)
            self.create_filelist_from_api(artifact_list_from_api=api_response)
            if self.artifact_file_details:
                self.start_download()
        else:
            print "Error {} \n url {}".format(session_response, self.artifact_url_complete)

    def run(self):

        #  SQL
        self.set_vertex_sql_properties()
        self.download_vertex_sql()
        print self.spacer_char_asterisk
        print "Service - SQL"
        self.show_downloaded_info()
        print self.spacer_char_asterisk
        self.clear_artifact_list()
        #  Service
        self.set_vertex_service_properties()
        self.download_vertex_service()
        print "Service - apps"
        self.show_downloaded_info()
        print self.spacer_char_asterisk
