import Database.Main_DB
import Utility
import config
import os
import logging

# Note: the chosen language code is called: IETF language tag or BCP-47

# TODO:
"""
 * Add if else condition that dictate to which language to translate to, for example if the subtitles are in english
 translate to hebrew, if in japanese translate to english etc..
 * Add watchdog to observe changes in the subtitles directory
 * Need to decide how to deploy it, I want a UI, even a basic one. So, maybe a container that has a UI? Or just a simple program UI.
 I don't want it in Terminal (Bash). It limits options to what a user can choose.
"""


def search_content():
    """
    This method calls to start looking for subtitles directories
    :return: none
    """
    Utility.process_srt_file()

    # warns if letter count is too high
    digits = Database.Main_DB.get_latest_letter_count()
    logging.info("Letters translated: " + str(digits))

    # if digits >= 450000:
    # print("Careful, you might be blocked until the month ends")


# Configure logging for docker
logging.basicConfig(filename='/var/log/app.log', level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')

"""
# Configure logging for IDE debugging
logging.basicConfig(
    filename='log_file_name.log',
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
            logging.info("Appended directory "+path)
        elif os.path.isdir(path) and entry not in exclude_dirs:
            # Deep scan within the directory for any sub-directories that are mount points
            for root, dirs, files in os.walk(path):
                if os.path.ismount(root):
                    dynamic_mount_points.append(root)

    return dynamic_mount_points


# Uncomment below to run the function and find dynamic mount points
# print(find_dynamic_mount_points())


def main():
    logging.info("Starting main")
    dynamic_mount_points = find_dynamic_mount_points()
    Database.Main_DB.initialize_db()
    if len(Database.Main_DB.get_directories()) != len(dynamic_mount_points):
        # Default pathing point
        # C:\Users\Shaked\PycharmProjects\SubtitlesTranslator\subtitlesTest
        # The user inputted Mount_Path for the application
        Database.Main_DB.set_directories(dynamic_mount_points)
    logging.info("The location of the directory is: " + str(Database.Main_DB.get_directories()))

    config.target_language = os.getenv('TARGET_LANGUAGE', 'iw')
    logging.info("Chosen language to translate to: " + config.target_language)
    search_content()


if __name__ == "__main__":
    main()

# Uncomment below to run the function and find mount points
# print(find_mount_points())
