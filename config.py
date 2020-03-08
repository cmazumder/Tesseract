#  This is a configuration file for user to update download and setup preference

#  User to set what all can be downloaded for TeamCity artifacts
setup_choice = {
    "vertex": {
        "download": "yes",
        "setup": {
            "box": "yes",
            "pc": "no"}
    },
    "nabler": {  # future functionality, vertex only for now
        "download": "no",
        "setup": {
            "box": "no",
            "pc": "no"},
    },
    "buildTypeID": "yes",
    "tag": {
        "download": "no",  # future functionality, download using buildTypeID only for now
        "tags": ["Witness"]
    }
}
