# loan-word-detection
Paper: A Generalized Method for Automated Multilingual Loanword Detection
Authors: Abhijnan Nath, Sina Mahdipour Saravani, Ibrahim Khebour, Sheikh Mannan, Zihui Li, and Nikhil Krishnaswamy
Published at COLING 2022

* `supported_languages.txt` lists the languages our system currently supports in principle.  We have evaluated on English-French, English-German, Indonesian-Dutch, Polish-French, Romanian-French, Kazakh-Russian, Persian-Arabic, Romanian-Hungarian, German-French, Hindi-Persian, Finnish-Swedish, Azerbaijani-Arabic, Mandarin-English, Hungarian-German, German-Italian, and Catalan-Arabic.

## Pipeline
* Python 3.7 is recommended (Python 3.8+ caused errors with `googletrans` package).
* Specify language pairs and Wiktionary links in `language-pairs.json`.
  * Resources:
    * [EpiTran codes](https://github.com/dmort27/epitran#transliteration-languagescript-pairs)
    * [ISO 639-1 codes (for Google Translate)](https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes)
* Run `wiktionary-scraper-python/scraper.ipynb` to get L1-L2 loan pairs and homonyms for each pair.
* Run `wiktionary-scraper-python/scaper_lemmas.ipynb` to get all L2 lemmas.
* Run `Datasets/make-datasets.ipynb` (running on Colab will prompt you to upload all resource files, including scraped data; running locally will require you to move the `*-AllLemmas.csv` data files into `Datasets/AllLemmas`).
  * If running `make-datasets.ipynb` locally, move all downloaded files into the correct folders within `Datasets`.
  * Recommended to run `remove-overlaps.ipynb` to remove remaining overlaps between synonyms, hard negatives, and loans (occurs due to case sensitivity in Google Translate, will incorporate fix into `make-datasets.ipynb` for final release).
* Run `make-train-test-splits.ipynb`.
* Run `get-logits-cos_sims.ipynb` to train phonetic alignment networks and get logits and cosine similarities for each pair.
* Move any language pairs you want held out from the training into `language-pairs-holdout.json`.
* Run `evaluate-experiments.ipynb` to run evaluations!

## Extending Epitran
Not all languages supported by MBERT and XLM are supported by Epitran.  Luckily, it's simple to extend Epitran to another language if you know its orthography and sound pattern.  See David Mortensen's discussion [here](https://github.com/dmort27/epitran#extending-epitran-with-map-files-preprocessors-and-postprocessors).  We have provided sample additional map and preprocessing files for Finnish, a simple use case, in `epitran-extensions`.  These files would need to be moved into the corresponding folder in the Epitran distribution in your Python's `site-packages`.
