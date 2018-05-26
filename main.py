import math
import os
import docx
import subprocess
import collections

def getText(filename):
    doc = docx.Document('docx/' + filename + '.docx')
    fullText = []
    for para in doc.paragraphs:
        fullText.append(para.text)
    return '\n'.join(fullText)


def converttotxt(filename):
    f = open('txt/' + filename + '.txt', 'w', encoding='utf-8')
    f.write(getText(filename))
    f.close()

def mystem(filename):
    converttotxt(filename)
    args = 'mystem/mystem.exe -n -w -l -d  txt/' + filename + '.txt results/mystem/' + filename + '.txt'
    subprocess.call(args)

def compute_tf(text):
    tf_text = collections.Counter(text)
    for i in tf_text:
        tf_text[i] = tf_text[i] / float(len(text))
    return tf_text


def normilizer(filename):
    mystem(filename)
    f = open('results/mystem/' + filename + '.txt', 'r', encoding='utf-8')
    text = []
    for line in f:
        if '??' not in line:
            text.append(line.replace('\n', ''))
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
    return documents_list


def preparing_doc():
    directory = 'docx'
    files = []
    for word in os.listdir(directory):
        files.append(word.replace('.docx', ''))
    list_documents = []
    for name in files:
        list_documents.append(normilizer(name))
    return list_documents


if __name__ == '__main__':
    print(preparing_doc())