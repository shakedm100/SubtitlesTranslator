import os
import glob
import re

import Database.Main_DB
import Translator

def subtitles_folder_paths():
    """
        The following method finds all the .srt files in the set directory and all it's sub directories.
    :return: a list of all the subdirectories which contains the .srt files
    """
    subtitle_files = [] # Contains all the subtitles found

    # O(n^2) complexity to look at all the paths in the main folder
    for dirpath, _, _ in os.walk(Database.Main_DB.get_main_directory()):
        # Search for .srt files in the current directory
        for file in glob.glob(os.path.join(dirpath, '*.srt')):
            subtitle_files.append(file)

    return subtitle_files


def process_srt_file():
    file_paths = subtitles_folder_paths()
    """
    This method receives a list of file paths and translates chooses which line
    goes to translation and which line isn't.
    if the line is a timing line or an empty line it doesn't translate it, otherwise it does
    :param file_paths: The list of files that need to be translated
    :return: non
    """
    for file_path in file_paths:
        translated_lines = []

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
                elif line.isdigit() or line == '':
                    translated_lines.append(line)
                else:
                    translated_text = Translator.translate_line(line)
                    translated_lines.append(translated_text)

        # Extract the base name and the extension of the original file
        dir_path, base_name = os.path.split(file_path)
        name, ext = os.path.splitext(base_name)

        # Create the new filename with '_translated' suffix
        new_file_name = f"{name}_translated{ext}"

        # Construct the full path for the new file
        new_file_path = os.path.join(dir_path, new_file_name)

        # Write the translated content to the new SRT file
        with open(new_file_path, 'w', encoding='utf-8') as new_file:
            for translated_line in translated_lines:
                new_file.write(f"{translated_line}\n")