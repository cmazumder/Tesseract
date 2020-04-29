from website.api.application import Application


class DataService(Application):

    def __init__(self):
        Application.__init__(self)
        try:
            self.build_id = self.get_successful_buildid(
                build_type_id=teamcity_download_setting["dataservice"]["buildTypeID"])
            self.folder = artifacts_to_download["dataservice"]["folder_name"]
        except KeyError as err:
            print "Key error: {0}\nLists: {1}".format(err.message, err.args)
        except NameError as err:
            print "Name error: {0}\nLists: {1}".format(err.message, err.args)

    def __del__(self):
        pass

    def set_vertex_dataservice_properties(self):
        anchor_text = teamcity_download_setting["dataservice"]["anchor"]
        self.set_file_download_path(save_artifact_dir=self.folder)
        self.set_artifact_url(self.build_id, anchor_text)

    def download_vertex_dataservice(self):
        session_response = self.teamcity_session.get_url_response(self.artifact_url_complete,
                                                                  self.teamcity_session.username,
                                                                  self.teamcity_session.password)
        if session_response.status_code == 200:
            api_response = self.get_json_response_as_dict(self.artifact_url_complete)
            self.create_filelist_from_api(artifact_list_from_api=api_response)
            if self.artifact_file_details:
                self.start_download()
        else:
            print "Error {} \n url {}".format(session_response, self.artifact_url_complete)

    def run(self):

        self.set_vertex_dataservice_properties()
        self.download_vertex_dataservice()
        print self.spacer_char_asterisk
        print "DataService"
        self.show_downloaded_info()
        print self.spacer_char_asterisk
