from googletrans import Translator
import Database.Main_DB
import config

def translate_line(text):
    """
    receives text in send it to google translate based on the target language
    :param text: the string to be translated
    :return: the translated text
    """

    changed = False
    to_translate = check_special_character(text)
    if to_translate != text:
        changed = True

    translator = Translator()
    source_language = 'auto'
    translation = translator.translate(to_translate, config.target_language, source_language)

    if changed:
        translation.text = '<i>' + to_translate + '</i>'

    Database.Main_DB.update_letter_count(len(to_translate))
    return translation.text


def check_special_character(line):
    """
    Actually, not sure if I should keep this method or not.
    it removes the special characters from the line
    :param line: the line that will be trimmed
    :return: the new trimmed line
    """
    new_line = line.replace('<i>', '')
    new_line = new_line.replace('</i>', '')

    return new_line

