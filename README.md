# loan-word-detection
CSU SIGNAL Lab Loan Word MT Project

## Pipeline
* Specify language pairs and Wiktionary links in `wiktionary-scraper-python/links.json`
* Run `scraper_without_ipas.ipynb` to get loan pairs
* Run `scaper_false_friends.ipynb` to get false friend pairs
* Add script and language columns (TODO)
* Compute hard negatives (Ibrahim)
* Compute direct translations (Ibrahim)
* Compute randoms (Ibrahim?)
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
* Make training and testing distributions (Abhijnan)
* Run PanPhon classifiers over training distributions (Abhijnan)
* Extract PanPhon logits for all training and testing distributions (Abhijnan)
* Add PanPhon features and logits column (Abhijnan)
* Concatenate all languages for training
* Train
* Evaluate
