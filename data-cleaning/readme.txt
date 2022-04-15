Sina: I am including the script validator to this folder.
The code can be run as follows:
python script_detection.py input_dataset.csv

The 'input_dataset.csv' should follow the same name format as the files in the 'Datasets' folder; as an example, it should be 'Hindi-Persian-Hard-Negatives.csv'. The reason for this is that the code uses the terms 'Hindi' and 'Persian' from the file name to validate the script of 'loan_word' and 'original_word' columns of the input csv file.
