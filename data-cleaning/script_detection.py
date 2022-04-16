from unicodedata2 import unicodedata2
import pandas as pd
import sys


lang_script_dict = {'Persian': 'Arabic', 'Hindi': 'Devanagari', 'English': 'Latin'}


def validate_script(in_str, supposed_script):
    in_chars = list(in_str)
    # print(in_chars)
    script = unicodedata2.script(in_chars[0])
    if script != supposed_script:
        return False
    for ch in in_chars:
        char_script = unicodedata2.script(ch)
        if char_script != script:
            return False
    return True


if __name__ == '__main__':
    args = sys.argv
    # print(unicodedata2.script_cat('a'))
    # print(unicodedata2.script_cat('अ'))
    # print(unicodedata2.script('a'))
    # word = 'at͡ʃaːr ad͡ʒiːb d͡ʒɒzb d͡ʒbrɒً'
    # for i in word:
    #     print(i, ' ', unicodedata2.script(i))
    # exit()
    # list of characters = [*string]
    dataset_df = pd.read_csv(args[1])
    filename_elements = args[1].split('/')[-1].split('-')
    l1 = filename_elements[0]
    l2 = filename_elements[1]
    print("Len of dataset before processing: ", len(dataset_df))
    dataset_df.drop(dataset_df[dataset_df['loan_word'].apply(validate_script, supposed_script=lang_script_dict[l1]) == False].index, inplace=True)
    dataset_df.drop(dataset_df[dataset_df['original_word'].apply(validate_script, supposed_script=lang_script_dict[l2]) == False].index, inplace=True)
    print("Len of dataset after processing: ", len(dataset_df))
    dataset_df.to_csv(args[1][:-4]+'-corrected.csv')


