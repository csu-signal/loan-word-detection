Scraped the following Wikipedia link:
https://en.wikipedia.org/wiki/List_of_languages_by_writing_system

'get_lang_scripts.py' is the python code that scrapes the link; however, I am not sure if we need it or not (I pushed it in case).
the only dependency is BeautifulSoup:
  pip install beautifulsoup4


The 'language_scripts.csv' file contains the data from that link in the following format:

language, script
Persian, Arabic script
English, Latin script
...
