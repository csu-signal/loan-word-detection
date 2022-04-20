# Wiktionary scraper

## how to run

* add the language pairs to be scraped in the links.json file. Following is an example of a valid json where we look for Persian terms that are borrowed into Hindi: 
    * {
    "Hindi-Persian" : "https://en.m.wiktionary.org/wiki/Category:Hindi_terms_borrowed_from_Persian"
    }

* run the scraper notebook as it is. The result file will contain the word in language 1 e.g hindi, the word borrowed from language 2, the IPAs as how the word is pronounced in language 1. 

## possible issues

* May get time outs due to continuously requesting web pages from wictionary. Can include sleep conditions. This will prompt the code to return all words extracted so far. 

## requirements

* python 3.7 or above
* requests, bs4, tqdm, unicodeblock