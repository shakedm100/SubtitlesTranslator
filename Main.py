import Database.Main_DB
import Utility
import config

# Note: the chosen language code is called: IETF language tag or BCP-47

# TODO:
"""
 * Add if else condition that dictate to which language to translate to, for example if the subtitles are in english
 translate to hebrew, if in japanese translate to english etc..
 * Containerize the shit out of this project.
 * Need to decide how to deploy it, I want a UI, even a basic one. So, maybe a container that has a UI? Or just a simple program UI.
 I don't want it in Terminal (Bash). It limits options to what a user can choose.
"""

def main():
    Database.Main_DB.initialize_db()
    if Database.Main_DB.get_main_directory() is None:
        dir = input("Set a main directory to search subtitles!")
        Database.Main_DB.set_main_directory(dir)
    config.target_language = input("Choose language")
    Utility.process_srt_file()

    digits = Database.Main_DB.get_latest_letter_count()
    print(digits)

    if digits >= 450000:
        print("Careful, you might be blocked until the month ends")


main()

