# loan-word-detection
CSU SIGNAL Lab Loan Word MT Project

* `supported_languages.txt` lists the languages our system currently supports in principle.  We have evaluated on {add languages here}.

## Pipeline
* Specify language pairs and Wiktionary links in `language-pairs.json`
  * Resources:
    * [EpiTran codes](https://github.com/dmort27/epitran#transliteration-languagescript-pairs)
    * [Google Translate codes](https://www.labnol.org/code/19899-google-translate-languages#google-translate-languages)
* Run `wiktionary-scraper-python/scraper.ipynb` to get L1-L2 loan pairs and false friends for each pair 
* Run `wiktionary-scraper-python/scaper_lemmas.ipynb` to get false friend pairs
* Run `Datasets/make-datasets.ipynb` (running on Colab will prompt you to upload all resource files, including scraped data; running locally will require you to move the `*-AllLemmas.csv` data files into `Datasets/AllLemmas`.
  * If `make-datasets.ipynb` move all downloaded files into the correct folders within `Datasets`
* Run `make-train-test-splits.ipynb`
* Run `get-logits-cos_sims.ipynb` to train phonetic alignment networks and get logits for each pair
* Run `evaluate-experiments.ipynb` to run evaluations!

## Extending EpiTran
Not all languages supported by MBERT and XLM are supported by EpiTran.  Luckily, it's simple to extend EpiTran to another language if you know its orthography and sound pattern.  See David Mortensen's discussion [here](https://github.com/dmort27/epitran#extending-epitran-with-map-files-preprocessors-and-postprocessors).  We have provided sample additional map and preprocessing files for Finnish, a simple use case, in `epitran-extensions`.

### notes on false friends processing
* Process false friends (TODO)
* * remove all rows where source language is not supported by EpiTran/MBERT/XLM
* * reduce translations to single word (script drops all instances of "a", "the" or "to" at the beginning of a translation)
* Compute IPA (Ibrahim)
* Clean all datasets
* * remove rows with empty cells, words in the wrong script for the language, prefixes and suffixes (Ibrahim, Sina?)
* * clean up IPA transcriptions (language-dependent, we include scripts for ...) (Ibrahim, Sina?)
* * remove any overlaps between dataset (make sure no false friends or loans are in the hard negatives, direct translations, or randoms, make hard negatives, direct translations, and randoms are mutually exclusive) (Ibrahim)
* Compute all edit distances (Ibrahim)
* Compute MBERT and XLM pair similarities (Sina, Zihui, Abhijnan?)
* * compute pair similarities for false friends using L1-English instead of L1-L2? - probably don't need to do this if the meanings can be reduced to single words and we reduce the sample to only languages supported by MBERT/XLM
