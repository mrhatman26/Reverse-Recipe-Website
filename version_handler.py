import datetime as dt
from file_paths import VERSION_FILE_DIR

def get_version():
    version_file = open(VERSION_FILE_DIR, "w")
    version = version_file.readline()
    version_file.close()
    if version is not None:
        if version != "" and version.isspace() is False:
            return version
        else:
            return "(NO VERSION)"
    else:
        return "(NO VERSION)"
    
def update_version():
    version = dt.datetime.now()
    version = "(" + str(version.strftime(("%Y%m%d.%H%M%S"))) + ")"
    version_file = open(VERSION_FILE_DIR, "w")
    version_file.write(version)
    version_file.close()
    return version