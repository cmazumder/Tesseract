# ControllerSetup_from_TeamCity
Download and create package from team city and also do some housekeeping task

## Using Python framework
Pre-requisite: Need active internet connection to Aristocrat network. Since have to download builds from TeamCity

* Create a folder since here we will place all our requisite contents
* For this example, I have created a folder in environment at location F:\CM\Automation 
* Create another folder DeployBuilds_from_TeamCity or checkout the repository
* ![image info](.graphics/documentation/Framework_structure.png)
* To run the framework
Open Command Prompt and navigate to the root F:\CM\Automation\DeployBuilds_from_TeamCity
* Navigate to root of framework
* > cd /d F:\CM\Automation\DeployBuilds_from_TeamCity
* Typing the following command and hit ENTER
* > python main.py
>
* The python framework work based on Json configuration files and part of the download 
* These configs are placed in folder F:\CM\Automation\DeployBuilds_from_TeamCity\configuration

## Configurations
The python framework work based on Json configuration files and part of the download 
* These configs are placed in directory DeployBuilds_from_TeamCity\configuration
* Sample master config file config_path.json

Master config
> {
>  "_comment": "path to all configuration files",
>  "artifacts_to_download": "configuration/artifacts_to_download_VERTEX.json",
>  "environment_setting": "configuration/environment_setting_VERTEX.json",
>  "database_setting": "configuration/database_setting.json",
>  "teamcity_setting": "configuration/teamcity_setting.json"
> }

* User has to ensure these four configurations files are based on thier requirement and setup

* artifacts_to_download: Configuration information related to Vertex/NAbler or any other artifact information as per need.

Information of which build ID and tags (if supplied) to use from TeamCity
Where to replace the artifacts in the setup
What sort of configuration files are present, and needs to be copied to any specific location
Value is path of the config file. E.g. "configuration/artifacts_to_download_VERTEX.json"

Application details for Vertex Expand source
environment_setting: Environment specific information 

Information related to what file extensions to be ignored while downloading. 
Windows processes to terminate, to not cause issue when deleted old artifacts and copying downloaded artifacts
Which database to setup, and additional setting, if required.
Configuration files to modified for test environment. 
Value is path of the config file. E.g. "configuration/environment_setting_VERTEX.json"

Environment details for Vertex Expand source
database_setting: 

Database server and connection details for environment
Value is path of the config file. E.g. "configuration/database_setting.json"

Database connection details for Vertex Expand source
teamcity_setting:

TeamCity server and connection details
Value is path of the config file. E.g. "configuration/teamcity_setting.json"

Database connection details for Vertex Expand source
This is a one time activity, unless any update in Python framework. Frequency of update will be less
User should have to maintain/modify configuration files
NAbler and Vertex samples are already created
Vertex has two sample:
Trunk artifacts_to_download_VERTEX_trunk.json
Next artifacts_to_download_VERTEX_next.json