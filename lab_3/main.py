"""
Labour work #3
 Building an own N-gram model
"""

import math

REFERENCE_TEXT = ''
if __name__ == '__main__':
    with open('not_so_big_reference_text.txt', 'r') as f:
        REFERENCE_TEXT = f.read()


class WordStorage:
    def __init__(self):
        self.storage = {}

    def put(self, word: str) -> int:
        if word not in self.storage and isinstance(word, str):
            self.storage[word] = hash(word)
        return hash(word)

    def get_id_of(self, word: str) -> int:
        if word in self.storage and isinstance(word, str):
            return self.storage.get(word)
        return -1

    def get_original_by(self, id: int) -> str:
        if id in self.storage.values() and isinstance(id, int):
            for val1 in self.storage.items():
                if id == val1[1]:
                    return val1[0]
        return 'UNK'

    def from_corpus(self, corpus: tuple):
        if isinstance(corpus, tuple):
            for val in corpus:
                if val not in self.storage and isinstance(val, str):
                    self.storage[val] = hash(val)


class NGramTrie:
    def __init__(self, size):
        self.size = size
        self.gram_frequencies = {}
        self.gram_log_probabilities = {}

    def fill_from_sentence(self, sentence: tuple) -> str:
        if isinstance(sentence, tuple):
            for ind1 in range(len(sentence[:len(sentence)-self.size+1])):
                ind2 = ind1 + self.size
                newkey = sentence[ind1:ind2]
                if newkey not in self.gram_frequencies.keys():
                    self.gram_frequencies[newkey] = 1
                else:
                    self.gram_frequencies[newkey] += 1
                if not newkey:
                    return 'ERROR'
            return 'OK'

    def calculate_log_probabilities(self):
        for keys in self.gram_frequencies:
            keyvar = keys[:-1]
            count = 0
            for ind1, val1 in enumerate(list(self.gram_frequencies.keys())):
                if val1[:-1] == keyvar:
                    count += list(self.gram_frequencies.values())[ind1]
            self.gram_log_probabilities[keys] = math.log(self.gram_frequencies[keys]/count)

    def predict_next_sentence(self, prefix: tuple) -> list:
        if not isinstance(prefix, tuple):
            return []
        if len(prefix) != self.size - 1:
            return []
        mid_pref = []
        fin_pref = list(prefix)
        top_keys = sorted(self.gram_log_probabilities, key=self.gram_log_probabilities.__getitem__, reverse=True)
        while True:
            flag = False
            for val1 in top_keys:
                if val1[:-1] == prefix:
                    mid_pref = val1[-1]
                    fin_pref += [mid_pref]
                    flag = True
                    break
            if not flag:
                break
            new_pref = list(prefix[1:])
            new_pref.append(mid_pref)
            prefix = tuple(new_pref)
        return fin_pref

def encode(storage_instance, corpus) -> list:
    newlist = [[storage_instance.get_id_of(val) for val in corpus] for _ in range(1, len(corpus))]
    return newlist


def split_by_sentence(text: str) -> list:
    new_text1 = ''
    new_text = ''
    if not isinstance(text, str):
        return []
    text = text.replace('\n', '')
    text = text.replace('  ', ' ')
    text = text.replace('  ', ' ')
    for ind1, val1 in enumerate(text):
        new_text1 += val1
        if val1.isupper() and new_text1[ind1-1] == ' ':
            if new_text1[ind1-2] == '.' or new_text1[ind1-2] == '!' or new_text1[ind1-2] == '?':
                new_text1 = new_text1.replace('? ', '•◘')
                new_text1 = new_text1.replace('! ', '•◘')
                new_text1 = new_text1.replace('. ', '•◘')
    for val3 in new_text1.lower():
        if val3.isalnum() or val3 == ' ' or val3 == '•' or val3 == '◘':
            new_text += val3
    through_list = new_text.split('•◘')
    if len(through_list) == 1 or not new_text:
        return []
    new_list = []
    for val2 in through_list:
        new_list += [['<s>'] + val2.split(' ') + ['</s>']]
    return new_list
