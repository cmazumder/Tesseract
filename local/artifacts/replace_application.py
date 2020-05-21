from util import file_actions as File
from util import folder_actions as Folder


class ReplaceApplication:
    """
    Take care of replacement of binaries of applications
    """
    """
    application_replace_details - will save the information of the applications to be replaced
    AppName : {
                source: 'path',
                destination: [list of folder],
                status: True/False
                }
    """

    def __init__(self, app_source=None, app_destinations=None, config_source=None, config_destinations=None):
        self.app_source = app_source
        self.app_destinations = app_destinations
        self.config_source = config_source
        self.config_destinations = config_destinations
        self.status = None

    def _copy_folder(self):
        tmp_status = True
        for destination in self.app_destinations:
            if Folder.copy_from_to_location(source=self.app_source, destination=destination):
                if not self.__check_folder_copy_status(source=self.app_source, destination=destination):
                    tmp_status = False
            else:
                tmp_status = False
        return tmp_status

    def __check_folder_copy_status(self, source, destination):
        source_folder_property = Folder.get_folder_properties(source)
        destination_folder_property = Folder.get_folder_properties(destination)
        # compare between source and dest the count of files, sub folders and size
        if source_folder_property[0] == destination_folder_property[0] and \
                source_folder_property[0] == destination_folder_property[0] and \
                source_folder_property[0] == destination_folder_property[0]:
            return True
        else:
            return False

    def _copy_file(self):
        tmp_status = True
        for destination in self.config_destinations:
            if Folder.create_folder(destination):
                if File.copy_from_to_file(source=self.config_source, destination=destination):
                    if not self.__check_file_copy_status(source=self.config_source, destination=destination):
                        tmp_status = False
                else:
                    tmp_status = False
            else:
                tmp_status = False
        return tmp_status

    def __check_file_copy_status(self, source, destination):
        # compare source and dest file size
        if Folder.isdir(destination):
            destination = Folder.build_path(destination, File.basename(source))
        if not File.compute_file_size(source) == File.compute_file_size(destination):
            return True
        else:
            print "File size differ\n" \
                  "Source (size): {0} ({1})\n" \
                  "Destination (size): {2} ({3})".format(source, File.compute_file_size(source),
                                                  destination, File.compute_file_size(destination))
            return False

    def replace_artifact(self):
        tmp_status = True
        if self.app_source and self.app_destinations:
            if not self._copy_folder():
                tmp_status = False
                print "Could not replace folder\nSource:{}\nDestinations:{}".format(self.app_source,
                                                                                    self.app_destinations)
        if self.config_source and self.config_destinations:
            if not self._copy_file():
                tmp_status = False
                print "Could not replace file\nSource:{}\nDestinations:{}".format(self.config_source,
                                                                                  self.config_destinations)
        self.status = tmp_status

    def get_replace_status(self):
        return self.status
