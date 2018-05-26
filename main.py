import os
from sklearn.neighbors import KNeighborsClassifier
from nltk.corpus import stopwords
import numpy as np
import TF_IDF
import grade

def get_files_name():
    directory = 'docx'
    files = []
    for word in os.listdir(directory):
        files.append(word.replace('.docx', ''))
    return files


def preparing_doc(files):
    list_documents = []
    for name in files:
        f = open('results/mystem/' + name + '.txt', 'r', encoding='utf-8')
        text = []
        for line in f:
            text.append(line.replace('\n', ''))
        list_documents.append(text)
    print('finish preparing doc')
    return list_documents


def print_corpus(docs):
    f = open('final.txt', 'w', encoding='utf-8')
    for t in docs:
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


def compute_KNBHD(X_test, Y_test, X_predict):
    clf = KNeighborsClassifier(n_neighbors=4, weights="distance")
    clf.fit(X_test, Y_test)
    pred = clf.predict(X_predict)
    return pred


if __name__ == '__main__':
    file_names = get_files_name()
    docs = TF_IDF.compute_tf_idf(preparing_doc(file_names))
    words = prepare_word_set(docs)
    X_test = make_matrix([docs[0], docs[1], docs[2], docs[3], docs[4],
                          docs[11], docs[12],docs[20]], words)
    Y_test = ['SPEC','ANK', 'DOG', 'DOG', 'DOG', 'SPEC', 'SPEC', 'TREB']
    X_predict = make_matrix(docs, words)

    grade.counF(file_names,compute_KNBHD(X_test,Y_test, X_predict),"К ближайших соседей")









