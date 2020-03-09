from config.framework_config import application_structure, teamcity_download_setting
from teamcity.api.application import Application


class Reports(Application):

    def __init__(self):
        Application.__init__(self)
        try:
            self.build_id = self.get_buildId_from_buildTypeId(
                buildTypeId=teamcity_download_setting["reports"]["buildTypeID"])
            self.folder = application_structure["reports"]["folder_name"]
        except KeyError as err:
            print "Key error: {0}\nLists: {1}".format(err.message, err.args)
        except NameError as err:
            print "Name error: {0}\nLists: {1}".format(err.message, err.args)

    def __del__(self):
        pass

    def set_vertex_reports_properties(self):
        try:
            anchor_text = teamcity_download_setting["reports"]["anchor"]
            self.set_file_download_path(save_artifact_dir=self.folder)
            self.set_artifact_url(self.build_id, anchor_text)
        except KeyError as err:
            print "Key error: {0}\nLists: {1}".format(err.message, err.args)
        except NameError as err:
            print "Name error: {0}\nLists: {1}".format(err.message, err.args)

    def download_vertex_reports(self):
        session_response = self.teamcity_session.get_url_response(self.artifact_url_complete,
                                                                  self.teamcity_session.username,
                                                                  self.teamcity_session.password)
        if session_response.status_code == 200:
            api_response = self.get_decoded_json_response(self.artifact_url_complete)
            self.create_filelist_from_api(api_response=api_response)
            if self.artifact_file_details:
                self.start_download()
        else:
            print "Error {} \n url {}".format(session_response, self.artifact_url_complete)

    def run(self):
        self.set_vertex_reports_properties()
        self.download_vertex_reports()
        print self.spacer_char_asterisk
        print "Reports"
        self.show_downloaded_info()
        print self.spacer_char_asterisk
