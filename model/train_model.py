import os
from model.model import NgramLanguageModel_1

def train_model(input_file):
    model = NgramLanguageModel_1()
    model.train_method(input_file)
 
    model.perplexity()
    #print("Model trained and loaded into memory.")
    return model

if __name__ == '__main__':
   
    input_file = 'data/train.txt'  
  
    if not os.path.exists(input_file):
        print(f"The input file {input_file} does not exist. Please provide a training data file.")
    else:
        model = train_model(input_file)
