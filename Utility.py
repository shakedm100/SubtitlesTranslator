import os
import glob
import re
import Database.Main_DB
import Translator
import config
import logging


def subtitles_folder_paths():
    """
    The following method finds all the .srt files in the set directory and all it's sub directories.
    :return: a list of all the subdirectories which contains the .srt files
    """

    logging.info("Searching for sub folder paths")
    subtitle_files = []  # Contains all the subtitles found
    directory_list = Database.Main_DB.get_directories()
    logging.info("Directory list = "+str(directory_list)+ "the type is: "+str(type(directory_list)))
    try:
        for directory in directory_list:
            logging.info("currently searching directory = "+str(directory))
            # O(n^2) complexity to look at all the paths in the main folder
            for dirpath, _, _ in os.walk(directory):
                #logging.info("Walking")
                # Search for .srt files in the current directory
                for file in glob.glob(os.path.join(dirpath, '*.srt')):
                    subtitle_files.append(file)
    except:
        logging.info("ERROR: Failed to search directories")
    return subtitle_files


def process_srt_file():
    """
    This method receives a list of file paths and translates chooses which line
    goes to translation and which line isn't.
    if the line is a timing line or an empty line it doesn't translate it, otherwise it does
    :return: Void
    """

    logging.info("Processing srt files")

    file_paths = subtitles_folder_paths()
    for file_path in file_paths:
        if not is_already_translated(file_path):
            translated_lines = []
            all_redundancy = True  # Will check if the translation's redundant

            with open(file_path, 'r', encoding='utf-8') as file:

                for line in file:
                    line = line.strip()
                    r"""
                     Check if the line is timing line using a regular expression
                     r - a prefix before a regex indicating a raw string so \ is treated as a literal character
                     (ironically enough had to use r to not get an error for the backslashes)
                     \d is special character to show any num between [0,9]
                     {2} is the number of occurrences for an element
                     for example: 00:12:34,253 00 represents the first \d{2} and so on and 253 is \d{3}
                    """
                    if re.match(r'\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3}', line):
                        translated_lines.append(line)
                    elif line.startswith("# Translated-To-Language:"):
                        translated_lines.append(line)
                    elif line.isdigit() or line == '':
                        translated_lines.append(line)
                    else:
                        line_redundancy = Translator.check_redundant_translation(line)
                        all_redundancy = all_redundancy and line_redundancy  # If all of the lines are redundant it will return true all the way
                        if not line_redundancy:
                            translated_text = Translator.translate_line(line)
                            translated_lines.append(translated_text)

            # Extract the base name and the extension of the original file
            dir_path, base_name = os.path.split(file_path)
            name, ext = os.path.splitext(base_name)

            # Create the new filename with '_translated' suffix
            new_file_name = f"{name}_translated{ext}"

            # Construct the full path for the new file
            new_file_path = os.path.join(dir_path, new_file_name)

            # if all the lines are redundant don't make a new file
            if not all_redundancy:
                # Write the translated content to the new SRT file
                create_new_srt(new_file_path, translated_lines)

        add_translation_stamp(file_path)


def create_new_srt(new_file_path, translated_lines):
    with open(new_file_path, 'w', encoding='utf-8') as new_file:
        for translated_line in translated_lines:
            new_file.write(f"{translated_line}\n")


def add_translation_stamp(original_file_path):
    if not is_already_translated(original_file_path):
        with open(original_file_path, 'r+', encoding='utf-8') as file:
            content = file.read()
            file.seek(0, 0)
            file.write(f"# Translated-To-Language: {config.target_language}\n" + content)


def is_already_translated(original_file_path):
    """
    This method checks if the 'stamp' exists and checks if this is for the targeted language
    :param original_file_path: well, the original file path
    :return: True if the file was translated to the targeted language
    """
    with open(original_file_path, 'r', encoding='utf-8') as file:
        # Read the first few lines to look for the stamp
        for i in range(10):  # Adjust the range as needed based on stamp location
            line = file.readline()
            if line.startswith("# Translated-To-Language:"):
                i, language = line.strip().split(': ')
                return language == config.target_language
    return False


def was_translated_to(file_path):
    """
    The following method checks if the file was translated before
    :param file_path: the file to check
    :return: True if the file was translated
    """
    if "_translated" in file_path:
        return True

    return False
