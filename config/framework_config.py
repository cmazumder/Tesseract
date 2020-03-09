#  This is a configuration file for CreatePackageController framework

#  Application's teamcity info as build type id and anchor text. Dynamic based on user choice (Vertex / Nabler)
#  eg teamcity_download_setting = vertex_buildTypeID
teamcity_download_setting = {}

#  configuration for controller box
deployment_env_paths = {
    "exclude_file_extension": [".pdb"],  # comma separated list of file extensions not to be downloaded
    "path_download_root": r"C:\Test_TeamCity\Artifacts",  # local machine base path to download all the files
    "path_vertexApp": r"C:\Test_TeamCity\D_Drive",  # local machine base path to download all the files
    "path_vertexData": r"C:\Test_TeamCity\F_Drive",
    "config_folder": "Configurations",      # config files from all the apps to be saved in this folder
    "backup_folder": "Backup"
}

#  configuration for controller (local) database server
local_database_setting = {
    "db_server": "localhost\\SQLEXPRESS",
    "db_username": "sa",
    "db_password": "Password1",
    "db_size": {"reduce": "yes",
                "new_size": "100MB"},
    "db_to_delete": ['Vertex', 'VertexArch', 'GamesArch', 'Games', 'Misc'],
    "db_to_setup": "Vertex_and_Games_on_PC.sql",
}

#  configuration for TeamCity server
teamcity_setting = {
    "host": r"http://uslv-addv12-02.dev.local/",  # The host url TeamCity
    "teamcity_username": "guest",  # Login user name for TeamCity
    "teamcity_password": "guest",  # Login password for TeamCity
    "api_artifacts": r"/guestAuth/app/rest/builds/id:{0}/artifacts/children",
    "api_buildId": None,
}

# VertexApps D driver folder structure (common settings for Vertex and NAbler)
application_structure = {
    "service": {
        # Service info for Controller box setup
        "folder_name": "Service",
        "config_file_name": "Controller.config"},
    "ui": {
        # UI info for Controller box setup
        "folder_name": "UI",
        "config_file_name": "Web.config"},
    "shell": {
        # Shell info for Controller box setup
        "folder_name": "Shell",
        "config_file_name": "Shell.config"},
    "reports": {
        # Reports info for Controller box setup
        "folder_name": "Reports",
        "config_file_name": "Reports.config"},
    "dataservice": {
        # DataService info for Controller box setup
        "folder_name": "DataService",
        "config_file_name": "DataService.config"},
}

# Additional VertexApps D drive folder structure for NAbler
application_structure_nabler = {
    "auditui": {
        # Service info for Controller box setup
        "folder_name": "AuditUI",
        "config_file_name": None},
    "cms": {
        # UI info for Controller box setup
        "folder_name": "CMS",
        "config_file_name": "CmsDataService.config"},
    "ib": {
        # Shell info for Controller box setup
        "folder_name": "InterfaceBoardService",
        "config_file_name": "InterfaceBoardService.config"},
    "watchdog": {
        # Reports info for Controller box setup
        "folder_name": "Watchdog",
        "config_file_name": "Reports.config"},
    "valyria": {
        # DataService info for Controller box setup
        "folder_name": "Valyria",
        "config_file_name": "Valyria.config"}
}

#  configuration for TeamCity artifacts if build type used for vertex
vertex_buildTypeID = {
    "service": {  # BuildTypeID for Vertex Service
        "buildTypeID": "Vertex_Vertex_Trunk",
        "anchor": "Aristocrat.Vertex.Service"},
    "ui": {  # BuildTypeID for Vertex UI
        "buildTypeID": "Vertex_VertexUI_Trunk",
        "anchor": "Aristocrat.Vertex.UI.Web"},
    "shell": {  # BuildTypeID for Vertex Shell
        "buildTypeID": "Vertex_VertexShell_Trunk",
        "anchor": "VertexShell"},
    "reports": {  # BuildTypeID for Vertex Reports
        "buildTypeID": "Vertex_ReportsTrunk",
        "anchor": "Aristocrat.Vertex.Reports.Web"},
    "dataservice": {  # BuildTypeID for Vertex DataService
        "buildTypeID": "bt6",
        "anchor": "VertexDataService"}
}

process_to_stop = ['iexplore', 'WinMergeU']




