import docx
import subprocess
import collections
import sys

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


def tf(filename):
    f = open('results/mystem/' + filename + '.txt', 'r', encoding='utf-8')
    text = []
    for line in f:
        if '??' not in line:
            text.append(line.replace('\n', ''))
    return compute_tf(text)


if __name__ == '__main__':
    args = 'mystem/mystem.exe -n -w -l -d  txt/first.txt'
    with subprocess.call(args) as pse:
        text = []
        for line in pse:
            if '??' not in line:
                text.append(line.replace('\n', ''))
        print( compute_tf(text))




