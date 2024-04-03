import Database.Main_DB
import Translator
import Utility
import config

# Note: the chosen language code is called: IETF language tag or BCP-47

# TODO:
"""
 * Add if else condition that dictate to which language to translate to, for example if the subtitles are in english
 translate to hebrew, if in japanese translate to english etc..
 * Containerize the shit out of this project.
 * Think and add a way to let the program know that the file was translated and does not need to be translated again,
 Maybe some sort of a stamp?
"""

def main():
    Database.Main_DB.initialize_db()
    if(Database.Main_DB.get_main_directory() == None):
        dir = input("Set a main directory to search subtitles!")
        Database.Main_DB.set_main_directory(dir)
    config.target_language = input("Choose language")
    Utility.process_srt_file()

    print(Database.Main_DB.get_latest_letter_count())

main()

