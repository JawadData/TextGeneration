from collections import defaultdict, Counter
import os
import re
import string
import math
import random

class NgramLanguageModel_1:
    def __init__(self):
        self.bigram_counts = defaultdict(int)
        self.vocabulary = set()
        self.k = 0.01
        self.resultats = None
        self.word_freq = None
        self.train = None
        self.test = None
        self.ngram_size = 2
        self.words_autocomplete = []
        self.vocab_autocomplete = set()

    def prepare_data(self, infile):
        try:
            with open(infile, "r", encoding="utf-8") as file:
                sentences = [re.sub(r'[{}0-9]'.format(re.escape(string.punctuation)), '', sentence.strip().lower()) 
                            for sentence in file.readlines() if sentence.strip()]
        except FileNotFoundError:
            print("Fichier non trouvé ou impossible à lire.")
            sentences = [re.sub(r'[{}0-9]'.format(re.escape(string.punctuation)), '', infile.strip().lower())]
        
        for sentence in sentences:
            self.words_autocomplete.extend(sentence.split())
        
        self.vocab_autocomplete = set(self.words_autocomplete)
        
        processed_sentences = ["<s> " + sent + " </s>" for sent in sentences]
        
        train_size = int(len(processed_sentences) * 0.9)
        test_size = len(processed_sentences) - train_size

        train_sentences = processed_sentences[:train_size]
        test_sentences = processed_sentences[train_size:]

        words = [word for sentence in train_sentences for word in sentence.split()]
        
        self.word_freq = Counter(words)
        words = [word if self.word_freq[word] > 10 else "<UNK>" for word in words]
        self.vocabulary = set(words)
        self.train = ' '.join(words)
            
        self.test = ' '.join(test_sentences)

    def train_method(self, infile=""):
        self.prepare_data(infile)

        words = self.train.split()
        for i in range(len(words) - self.ngram_size + 1):
            bigram = tuple(words[i:i+2]) 
            self.bigram_counts[bigram] += 1
        
        self.resultats = {}

        print("Bigrammes comptés :")
        for bigram, count in self.bigram_counts.items():
            Wn_1 = bigram[0]
            C_Wn_1 = self.word_freq[Wn_1]
            C_Wn_1_Wn = count
            probability = (C_Wn_1_Wn + self.k) / (C_Wn_1 + self.k * len(self.vocabulary))
            log_probability = math.log(probability)
            self.resultats[bigram] = {'Probabilité': probability, 'Log Probabilité': log_probability}

        return self.resultats
    
    def predict(self, sentence):
        prep_sentences = [re.sub(r'[{}]'.format(re.escape(string.punctuation)), '', sentence.strip().lower())]

        processed_sentences = ["<s> " + sent + " </s>" for sent in prep_sentences]

        words = processed_sentences[0].split()
        bigram_predi = []
        res = 1

        for i in range(len(words) - self.ngram_size + 1):
            bigram = tuple(words[i:i+2])
            bigram_predi.append(bigram)
        for bigram in bigram_predi:
            if bigram in self.resultats:  
                prob = self.resultats[bigram]['Probabilité']
                res *= prob

        return math.log(res)
        
    def perplexity(self):       
        words = self.test.split()
        words_1 = [word for word in words if word != "<s>"]
        
        words = ' '.join(words_1)
        sents = words.split("</s>")
        token_count = len(words_1)
  
        log_prob_total = 0.0
        for line in sents:
            log_prob = self.predict(line)
            log_prob_total += log_prob

        avg_log_prob = log_prob_total / token_count
        perplexity = math.exp(-avg_log_prob)
        
        print("perp : ", perplexity)
        
        
    def autocomplete(self, input_text, max_words=100):
        if not self.resultats:
            print("Aucun modèle entraîné. Utilisez train_method d'abord.")
            return
        
        words = input_text.split()
        if len(words) < self.ngram_size - 1:
            print("Pas assez de mots pour générer un texte.")
            return
        
        generated_text = words[-self.ngram_size:] if self.ngram_size > 1 else [words[-1]]
        current_words = words[-self.ngram_size:] if self.ngram_size > 1 else [words[-1]]
        
        while len(generated_text) < max_words:
            candidates = []

            for bigram in self.resultats.keys():
                if bigram[0] == current_words[-1] and bigram[1] != "<UNK>":
                    candidates.append((bigram[1], self.resultats[bigram]['Probabilité']))
            
            if not candidates:
                break
            
            average_prob = sum([x[1] for x in candidates]) / len(candidates)

            filtered_candidates = [x[0] for x in candidates if x[1] >= average_prob]

            if filtered_candidates:
                next_word = random.choice(filtered_candidates)
            else:
                next_word = max(candidates, key=lambda x: x[1])[0]
           
            generated_text.append(next_word)
            
            if next_word == "</s>":
                break
            
            current_words = current_words[1:] + [next_word]
        
        generated_text = ' '.join(generated_text)
        
        if generated_text.endswith('</s>'):
            generated_text = generated_text[:-4].strip()
        print("Texte généré :", generated_text)
        return generated_text
