WIP!!

This is going to be an SRT subtitles translator. 
Currently, in version 0.1.
The end goal here is that anyone can take subtitles from one language and translate it to the desired one.

Current features:
* Translates all .srt files in a given subdirectory from one language to the requested language
* Adds a 'stamp' to check if the file was translated before, so it won't translate again
* Uses Google Translate API to do all the translating
* Gives a warning after 450,000 characters in a month, I don't really know google's cap and if there is one. But I saw from some source that it is 500,000 so better safe than sorry!

Development roadmap:
* Figure out how to deploy the program (Preferably with a UI)
* Add the option to give a use-case for any given language; for example if you want specifically Japanese subtitles to translate to English but Bulgarian to Polish
* Maybe add an ASS and PGS converter to SRT


* Note: currently to make the program re-translate you need to manually remove the 'stamp' from the original translation file.
the method for it is already written, but I'm not sure how to create a user friendly way to implement it.