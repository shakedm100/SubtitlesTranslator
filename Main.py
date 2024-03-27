import Utility

# Note: the chosen language code is called: IETF language tag or BCP-47

# TODO:
"""
 * A basic database that:
    * Count the number of characters this month, reset it every month, I think the cap is 500,000 chars per month for free
    * Store the main folder location
 * Currently translates to hebrew automatically, needs to change it to any language and think of a user friendly way to do it
 * Add if else condition that dictate to which language to translate to, for example if the subtitles are in english
 translate to hebrew, if in japanese translate to english etc..
 * Containarize the shit out of this project.
 * Think and add a way to let the program know that the file was translated and does not need to be translated again,
 Maybe some sort of a stamp?
 * Add a way to ignore special character such as <i> and more
"""
def main():
    directory = input("Enter a directory to pick a subtitle .srt file from:")
    Utility.MAIN_FOLDER_PATH = directory
    testDirectory = Utility.folder_path()
    Utility.process_srt_file(testDirectory)
    print(testDirectory)

main()

