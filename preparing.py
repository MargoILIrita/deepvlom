import docx
import subprocess
import main


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
    print('finish mystem ' + filename)


if __name__ == '__main__':
    for i in main.get_files_name():
        mystem(i)
    print("Finished preparing")