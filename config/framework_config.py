#  This is a configuration file of CreatePackageController framework for VERTEX BOX

#  Application's teamcity info as build type id and anchor text. Dynamic based on user choice (Vertex / Nabler)
#  eg teamcity_download_setting = vertex_buildTypeID

Environment = "PROD"

teamcity_download_setting = {}

#  configuration for controller box
deployment_env_paths = {
    "exclude_file_extension": [".pdb"],  # comma separated list of file extensions not to be downloaded
    "path_download_root": r"F:\Artifacts",  # local machine base path to download all the artifact files
    "path_vertexApp": r"D:\\",  # local machine base path to vertex applications folder
    "path_vertexData": r"F:\\",  # local machine base path to vertex data folder
    "config_folder": "Configurations",  # config folder name, which is common in VertexApps and VertexData
    "backup_folder": "Backup"  # backup folder in VertexApps
}

#  configuration for controller (local) database server
local_database_setting = {
    "db_server": "localhost\\SQLEXPRESSq",
    "db_username": "sa",
    "db_password": "Password1",
    "db_size": {"reduce": "no",
                "new_size": "100MB"},
    "db_to_delete": ['Vertex', 'VertexArch', 'GamesArch', 'Games', 'Misc'],
    "db_to_setup": "Vertex_and_Games_on_VertexBox.sql",
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

process_to_stop = ['VertexShell.exe', 'Aristocrat.Vertex.Service.exe']
