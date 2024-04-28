import Database.Main_DB
import Utility
import config
import os
import logging
from app import create_app

# Note: the chosen language code is called: IETF language tag or BCP-47

# TODO:
"""
 * Add if else condition that dictate to which language to translate to, for example if the subtitles are in english
 translate to hebrew, if in japanese translate to english etc..
 * Add watchdog to observe changes in the subtitles directory
 * Add a UI, even a basic one. So, maybe a container that has a UI? Or just a simple program UI.
 I don't want it in Terminal (Bash). It limits options to what a user can choose.
 * Add a PGS/ASS to .srt file
"""

# Configure logging for docker
logging.basicConfig(filename='/var/log/app.log', level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s', force=True)

app = create_app()


def search_content():
    """
    This method calls to start looking for subtitles directories
    :return: none
    """
    Utility.process_srt_file()

    # warns if letter count is too high
    digits = Database.Main_DB.get_latest_letter_count()

    # if digits >= 450000:
    # print("Careful, you might be blocked until the month ends")


"""
# Configure logging for IDE debugging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s',
    datefmt='%H:%M:%S'
)
"""


def find_dynamic_mount_points():
    """
    Could not find a way to directly receive the user inputted mounted volume to the container
    So instead I search all the folders that are typically found in an alpine distribution
    Which the container is based on.
    Saves runtime for the searching process later
    :return: a list of all the none os mounted directories
    """
    # Exclude list for common system directories not typically used for user mounts
    exclude_dirs = {'bin', 'boot', 'dev', 'etc', 'home', 'lib', 'lib64',
                    'opt', 'proc', 'root', 'run', 'sbin', 'srv', 'sys',
                    'tmp', 'usr', 'var'}

    dynamic_mount_points = []
    # Start at the root directory and scan for potential mount points
    for entry in os.listdir('/'):
        path = f"/{entry}"
        # Exclude typical system paths and check if the path is a mount point
        if entry not in exclude_dirs and os.path.ismount(path):
            dynamic_mount_points.append(path)
            logging.info("Appended directory " + path)
        elif os.path.isdir(path) and entry not in exclude_dirs:
            # Deep scan within the directory for any subdirectories that are mount points
            for root, dirs, files in os.walk(path):
                if os.path.ismount(root):
                    dynamic_mount_points.append(root)

    return dynamic_mount_points


def main():
    logging.info("Starting main")

    # Find all the non OS mounted paths in the container
    dynamic_mount_points = find_dynamic_mount_points()
    Database.Main_DB.initialize_db()
    if len(Database.Main_DB.get_directories()) != len(dynamic_mount_points):
        # C:\Users\Shaked\PycharmProjects\SubtitlesTranslator\subtitlesTest
        Database.Main_DB.set_directories(dynamic_mount_points)

    config.target_language = os.getenv('TARGET_LANGUAGE', 'iw')

    search_content()
    app.run(host='0.0.0.0', port=5000, debug=True)


if __name__ == main():
    main()
    app.run(host='0.0.0.0', port=5000, debug=True)
