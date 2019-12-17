import math


REFERENCE_TEXTS = []


def clean_tokenize_corpus(texts_corpus: list) -> list:
    if not texts_corpus or not isinstance(texts_corpus, list):
        return []
    clean_token_corpus = []
    for one_text in texts_corpus:
        if one_text and isinstance(one_text, str):
            while '<br />' in one_text:
                one_text = one_text.replace("<br />", " ")
            clean_token_text = []
            words = one_text.split(" ")
            for word in words:
                new_word = ""
                if not word.isalpha():
                    for i in word.lower():
                        if i.isalpha():
                            new_word += i
                    if new_word:
                        clean_token_text.append(new_word.lower())
                else:
                    clean_token_text.append(word.lower())
            clean_token_corpus += [clean_token_text]
    return clean_token_corpus


class TfIdfCalculator:
    def __init__(self, corpus):
        self.corpus = corpus
        self.tf_values = []
        self.idf_values = {}
        self.tf_idf_values = []
        self.file_names = ['5_7.txt', '15_2.txt', '10547_3.txt', '12230_7.txt']

    def calculate_tf(self):
        if isinstance(self.corpus, list):
            for doc in self.corpus:
                if isinstance(doc, list):
                    sample_dic = {}
                    word_amount = len(doc)
                    for word in doc:
                        if not isinstance(word, str):
                            word_amount -= 1
                    for word in doc:
                        if isinstance(word, str) and word not in sample_dic:
                            word_quantity = doc.count(word)
                            sample_dic[word] = word_quantity/word_amount
                    self.tf_values += [sample_dic]
        return self.tf_values

    def calculate_idf(self):
        if isinstance(self.corpus, list):
            docs_len = len(self.corpus)
            word_count_dic = {}
            single_word_list = []
            for doc1 in self.corpus:
                if not isinstance(doc1, list):
                    docs_len -= 1
                if isinstance(doc1, list):
                    for word in doc1:
                        if isinstance(word, str) and word not in single_word_list:
                            single_word_list += [word]
            for word1 in single_word_list:
                if single_word_list:
                    for doc in self.corpus:
                        if not doc:
                            continue
                        if isinstance(doc, list):
                            if word1 in doc:
                                if word1 in word_count_dic:
                                    word_count_dic[word1] += 1
                                else:
                                    word_count_dic[word1] = 1
                if word_count_dic[word1] != 0:
                    self.idf_values[word1] = math.log(docs_len/word_count_dic[word1])
        return self.idf_values

    def calculate(self):
        if self.idf_values and self.tf_values:
            for tf_in_one_doc in self.tf_values:
                new_tf_idf = {}
                for key, value in tf_in_one_doc.items():
                    new_tf_idf[key] = value * self.idf_values.get(key)
                self.tf_idf_values.append(new_tf_idf)
        return self.tf_idf_values

    def report_on(self, word, document_index):
        if not self.tf_idf_values or len(self.tf_idf_values) <= document_index:
            return ()
        working_dic = self.tf_idf_values[document_index]
        tf_idf_sorted = sorted(working_dic, key=working_dic.__getitem__, reverse=True)
        if word in self.corpus[document_index]:
            new_tuple = tuple([working_dic.get(word)] + [tf_idf_sorted.index(word)])
            return new_tuple

    def dump_report_csv(self):
        with open("report.csv", "w", encoding="utf-8") as dump_csv:
            tf_string = ''
            tf_idf_string = ''
            for nomen1 in self.file_names:
                tf_string += 'TF_' + nomen1 + ','
                tf_idf_string += 'TF-IDF_' + nomen1 + ','
            first_line = 'Word,' + tf_string + 'IDF,' + tf_idf_string[:-1]
            dump_csv.write(first_line)
            used_word_storage = []
            for doc in self.corpus:
                for word in doc:
                    lines = '\n'
                    if word in used_word_storage:
                        continue
                    if word not in used_word_storage:
                        lines += word
                    for index1 in range(len(self.tf_values)):
                        lines += ','
                        if word in self.tf_values[index1]:
                            lines += str(self.tf_values[index1][word])
                        else:
                            lines += '0'
                    lines += ',' + str(self.idf_values[word])
                    for index2 in range(len(self.tf_idf_values)):
                        lines += ','
                        if word in self.tf_idf_values[index2]:
                            lines += str(self.tf_idf_values[index2][word])
                        else:
                            lines += '0'
                    used_word_storage += [word]
                    dump_csv.write(lines)

    def cosine_distance(self, index_text_1, index_text_2):
        if not self.tf_idf_values or len(self.tf_idf_values) <= index_text_1 or len(self.tf_idf_values) <= index_text_2:
            return 100000000
        text_1 = self.corpus[index_text_1]
        text_2 = self.corpus[index_text_2]
        tf_idf_text_1 = self.tf_idf_values[index_text_1]
        tf_idf_text_2 = self.tf_idf_values[index_text_2]
        word_list = []
        value_list1 = []
        value_list2 = []
        for word1 in text_1:
            if isinstance(word1, str) and word1 not in word_list:
                word_list += [word1]
        for word2 in text_2:
            if isinstance(word2, str) and word2 not in word_list:
                word_list += [word2]
        for word3 in word_list:
            if word3 in text_1:
                value_list1 += [tf_idf_text_1.get(word3)]
            else:
                value_list1 += [0]
        for word4 in word_list:
            if word4 in text_2:
                value_list2 += [tf_idf_text_2.get(word4)]
            else:
                value_list2 += [0]
        num = 0
        denum1 = 0
        denum2 = 0
        for ind, val in enumerate(value_list1):
            num += val * value_list2[ind]
            denum1 += val * val
            denum2 += value_list2[ind] * value_list2[ind]
        denum = math.sqrt(denum1) * math.sqrt(denum2)
        cos_length = num/denum
        return cos_length


if __name__ == '__main__':
    texts = ['5_7.txt', '15_2.txt', '10547_3.txt', '12230_7.txt']
    for text in texts:
        with open(text, 'r') as f:
            REFERENCE_TEXTS.append(f.read())
    # scenario to check your work
    test_texts = clean_tokenize_corpus(REFERENCE_TEXTS)
    tf_idf = TfIdfCalculator(test_texts)
    tf_idf.calculate_tf()
    tf_idf.calculate_idf()
    tf_idf.calculate()
    tf_idf.dump_report_csv()
    print(tf_idf.report_on('good', 0))
    print(tf_idf.report_on('and', 1))
    print(tf_idf.cosine_distance(1, 2))
