import math
import os
import collections

from sklearn.neighbors import KNeighborsClassifier
from nltk.corpus import stopwords
import numpy as np

def compute_tf(text):
    tf_text = collections.Counter(text)
    for i in tf_text:
        tf_text[i] = tf_text[i] / float(len(text))
    return tf_text


def normilizer(filename):
    f = open('results/mystem/' + filename + '.txt', 'r', encoding='utf-8')
    text = []
    for line in f:
        if '??' not in line:
            text.append(line.replace('\n', ''))
    print('finish normilizer ' + filename)
    return text


def compute_idf(word, corpus):
    return math.log10(len(corpus) / sum([1.0 for i in corpus if word in i]))


def compute_tf_idf(corpus):
    documents_list = []
    for text in corpus:
        tf_idf_dictionary = {}
        computed_tf = compute_tf(text)
        for word in computed_tf:
            tf_idf_dictionary[word] = computed_tf[word] * compute_idf(word, corpus)
        documents_list.append(tf_idf_dictionary)
    print('finish compute_tf_idf')
    return documents_list

def get_files_name():
    directory = 'docx'
    files = []
    for word in os.listdir(directory):
        files.append(word.replace('.docx', ''))
    return files


def preparing_doc(files):
    list_documents = []
    for name in files:
        list_documents.append(normilizer(name))
    print('finish preparing doc')
    return list_documents


def print_corpus(corpus):
    f = open('final.txt', 'w', encoding='utf-8')
    for t in compute_tf_idf(corpus):
        for key in t:
            f.write('{0} = {1}\n'.format(key, t[key]))
        f.write('\nNext doc\n')
    f.close()

def prepare_word_set(docs):
    words = set()
    for dictionary in docs:
        words.update(dictionary)
    stop_words = stopwords.words('russian')
    stop_words.extend(['что', 'это', 'так', 'вот', 'быть', 'как', 'в', '—', 'к', 'на'])
    return [i for i in words if ( i not in stop_words )]


def make_matrix(docs, words):
    X = np.zeros((len(docs), len(words)))
    for d in docs:
        for w in words:
            try:
                X[docs.index(d), words.index(w)] = d[w]
            except:
                X[docs.index(d), words.index(w)] = 0
    return X


def set_of_label(label, dict):
    result = set()
    for key, value in dict.items():
        if value == label: result.add(key)
    return result

if __name__ == '__main__':
    file_names = get_files_name()
    docs = compute_tf_idf(preparing_doc(get_files_name()))
    clf = KNeighborsClassifier(n_neighbors=4,weights="distance")
    words = prepare_word_set(docs)
    X_test = make_matrix([docs[0], docs[1], docs[2], docs[3], docs[4],
                          docs[11], docs[12],docs[20]], words)
    Y_test = ['SPEC','ANK', 'DOG', 'DOG', 'DOG', 'SPEC', 'SPEC', 'TREB']
    clf.fit(X_test, Y_test)
    pred = clf.predict(make_matrix(docs, words))
    labels = ['SPEC','ANK', 'DOG', 'TREB']
    right_labels = {'s1':'SPEC','s2':'SPEC', 's3':'SPEC',
                    's4':'SPEC', 's5':'SPEC', 's6':'SPEC',
                    's7':'SPEC', 's8':'SPEC', 's9':'SPEC','a1':'ANK',
                    'd1':'DOG', 'd2':'DOG', 'd3':'DOG', 'd4':'DOG', 'd5':'DOG',
                    'd6':'DOG', 'd7':'DOG', 'd8':'DOG', 'd9':'DOG', 'd10':'DOG',  't1':'TREB'}
    nn_labels = {file_names[i]: pred[i] for i in range(len(file_names))}
    for label in labels:
        print(label)
        set_right = set_of_label(label, right_labels)
        print('Правильный {0}'.format(set_right))
        set_clf = set_of_label(label, nn_labels)
        print('Классифицированный {0}'.format(set_clf))
        common_set = set_right.intersection(set_clf)
        print('Пересечение {0}'.format(common_set))
        r = len(common_set)/len(set_right)
        p = len(common_set)/len(set_clf)
        f = 2*p*r/(p+r)
        print('F мера для {0} = {1}\n\n'.format(label, f))






