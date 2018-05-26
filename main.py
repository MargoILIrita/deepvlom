import docx
import subprocess
import collections
import sys

#получение текста из docx
def getText(filename):
    doc = docx.Document('docx/' + filename + '.docx')
    fullText = []
    for para in doc.paragraphs:
        fullText.append(para.text)
    return '\n'.join(fullText)


#получение файла txt
def converttotxt(filename):
    f = open('txt/' + filename + '.txt', 'w', encoding='utf-8')
    f.write(getText(filename))
    f.close()


#запуск mystem плучение лемм
def mystem(filename):
    converttotxt(filename)
    args = 'mystem/mystem.exe -n -w -l -d  txt/' + filename + '.txt results/mystem/' + filename + '.txt'
    subprocess.call(args)


def compute_tf(text):
    tf_text = collections.Counter(text)
    for i in tf_text:
        tf_text[i] = tf_text[i] / float(len(text))
    return tf_text


if __name__ == '__main__':
    args = 'mystem/mystem.exe -n -w -l -d  txt/first.txt'
    with subprocess.call(args) as pse:
        text = []
        for line in pse:
            if line.find("??") != -1:
                text.append(line.replace('\n', ''))
        print(compute_tf(text))




