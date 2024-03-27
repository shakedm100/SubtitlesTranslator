from googletrans import Translator

def translate_line(text, target_language):
    """
    receives text in send it to google translate based on the target language
    :param text: the string to be translated
    :param target_language: the language which the translator will translate to
    :return: the translated text
    """
    translator = Translator()
    source_language = 'auto'
    translation = translator.translate(text, target_language, source_language)

    return translation.text