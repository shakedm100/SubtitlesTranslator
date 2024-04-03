from googletrans import Translator
import Database.Main_DB
import config


def translate_line(text):
    """
    receives text in send it to google translate based on the target language
    :param text: the string to be translated
    :return: the translated text
    """
    translator = Translator()
    if check_redundant_translation(text):
        return text

    source_language = 'auto'
    translation = translator.translate(text, config.target_language, source_language)

    Database.Main_DB.update_letter_count(len(text))
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


def get_original_language(line):
    translator = Translator()
    return translator.detect(line).lang


def check_redundant_translation(to_translate):
    translator = Translator()
    origin_language = translator.detect(to_translate)
    if origin_language.lang == config.target_language:
        return True

    return False
