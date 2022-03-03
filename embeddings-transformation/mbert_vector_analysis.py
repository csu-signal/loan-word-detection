# Author: Sina Mahdipour Saravani
# Link to our paper for this project:
#
import sys
import json
import torch
from transformers import BertTokenizer, BertModel, AdamW, get_linear_schedule_with_warmup, BertForSequenceClassification\
    , BertForPreTraining, AutoModel
from torch.utils.data import DataLoader
import numpy as np
import random
from myutils import load_data, myprint, MyDataset, MyDataset1

# Setting manual seed for various libs for reproducibility purposes.
torch.manual_seed(7)
random.seed(7)
np.random.seed(7)
# Setting PyTorch's required configuration variables for reproducibility.
torch.backends.cudnn.benchmark = False
torch.backends.cudnn.deterministic = True
torch.use_deterministic_algorithms(True)
# To run the code in a reproducibale way, use the following running parameter for CUDA 10.2 or higher:
# CUBLAS_WORKSPACE_CONFIG=:16:8 python tbinv_earlystop.py
# If you do not care about reproducibility, you can comment above configs and run the script without the parameter

# Path to data. Make sure you edit them properly to point to your local
# datasets.

# If you want to load an already fine-tuned model and continue its training, uncomment and edit the following line.
# LOAD_PATH = "/s/lovelace/c/nobackup/iray/sinamps/claim_project/2021-06-01_models/jun10_tbinv_ensemble_with_bigger_batch-final-epoch-15"

# Configuration variables to choose the pre-trained model you want to use and other training settings:
# the pre-trained model name from huggingface transformers library names:
PRE_TRAINED_MODEL = 'bert-base-multilingual-cased'
# it can be from the followings for example: 'digitalepidemiologylab/covid-twitter-bert-v2',
#                                            'bert-large-uncased',
#                                            'vinai/bertweet-base'
#                                            'xlnet-base-cased'

MAXTOKENS = 5
NUM_EPOCHS = 2000  # default maximum number of epochs
BERT_EMB = 768  # set to either 768 or 1024 for BERT-Base and BERT-Large models respectively
BS = 8  # batch size
INITIAL_LR = 1e-5  # initial learning rate
save_epochs = [1, 2, 3, 4, 5, 6, 7]  # these are the epoch numbers (starting from 1) to test the model on the test set
# and save the model checkpoint.
EARLY_STOP_PATIENCE = 30  # If model does not improve for this number of epochs, training stops.

# Setting GPU cards to use for training the model. Make sure you read our paper to figure out if you have enough GPU
# memory. If not, you can change all of them to 'cpu' to use CPU instead of GPU. By the way, two 24 GB GPU cards are
# enough for current configuration, but in case of developing based on this you may need more (that's why there are
# three cards declared here)
CUDA_0 = 'cuda:1'
CUDA_1 = 'cuda:1'
CUDA_2 = 'cuda:1'


if __name__ == '__main__':
    args = sys.argv
    epochs = NUM_EPOCHS
    # logfile = open('log_file_' + args[0].split('/')[-1][:-3] + str(time.time()) + '.txt', 'w')
    # myprint("Please wait for the model to download and load sub-models, getting a few warnings is OK.", logfile)
    # train_l1_texts, train_l2_texts = load_data(TRAIN_PATH)
    l1 = ["کتاب", "کتاب", "کتاب", "کتاب", "کتاب", "کتاب"]
    l2 = ["book", "food", "notebook", "rug", "किताब", "पुस्तक"]
    with torch.no_grad():
        tokenizer = BertTokenizer.from_pretrained(PRE_TRAINED_MODEL)
        tokenizer.model_max_length = MAXTOKENS
        l1_encodings = tokenizer(l1, truncation=True, padding='max_length', max_length=MAXTOKENS)
        l2_encodings = tokenizer(l2, truncation=True, padding='max_length', max_length=MAXTOKENS)
        dataset = MyDataset(l1_encodings, l2_encodings)
        data_loader = DataLoader(dataset, batch_size=BS, shuffle=False)  # shuffle False for reproducibility
        base_model = BertModel.from_pretrained(PRE_TRAINED_MODEL).to(CUDA_0)
        base_model.eval()
        cos_s = torch.nn.CosineSimilarity()
        print("\n\n\n\n")
        for step, batch in enumerate(data_loader):
            l1_vector = base_model(batch['l1_input_ids'].to(CUDA_0),
                                          attention_mask=batch['l1_attention_mask'].to(CUDA_0),
                                          return_dict=True).last_hidden_state[:, 1, :]
            l2_vector = base_model(batch['l2_input_ids'].to(CUDA_0),
                                          attention_mask=batch['l2_attention_mask'].to(CUDA_0),
                                          return_dict=True).last_hidden_state[:, 1, :]
            sims = cos_s(l1_vector, l2_vector).data.cpu().numpy()
            print("Similarities: ")
            for i in range(len(l1)):
                print(l1[i], ' and ', l2[i], ' : ', sims[i])
        while (True):
            print("\n")
            l1 = input("Enter the word in lang 1: ")
            l2 = input("Enter the word in lang 2: ")
            l1_encodings = tokenizer(l1, truncation=True, padding='max_length', max_length=MAXTOKENS)
            l2_encodings = tokenizer(l2, truncation=True, padding='max_length', max_length=MAXTOKENS)
            l1d = MyDataset1(l1_encodings)
            l2d = MyDataset1(l2_encodings)
            l1i = torch.unsqueeze(l1d[:]['input_ids'], 0)
            l1a = torch.unsqueeze(l1d[:]['attention_mask'], 0)
            l2i = torch.unsqueeze(l2d[:]['input_ids'], 0)
            l2a = torch.unsqueeze(l2d[:]['attention_mask'], 0)
            l1_vector = base_model(l1i.to(CUDA_0),
                                   attention_mask=l1a.to(CUDA_0),
                                   return_dict=True).last_hidden_state[:, 1, :]
            l2_vector = base_model(l2i.to(CUDA_0),
                                   attention_mask=l2a.to(CUDA_0),
                                   return_dict=True).last_hidden_state[:, 1, :]
            print("Similarities between " + l1 + " and " + l2 + " is ", cos_s(l1_vector, l2_vector).data.cpu().numpy())
    # End of main

