import re

import docx
import subprocess

import ezodf

import main


def getText(filename):
    doc = docx.Document('docx/' + filename + '.docx')
    fullText = []
    for para in doc.paragraphs:
        fullText.append(para.text)
    return '\n'.join(fullText)


def getODTText(filename):
    odt = ezodf.opendoc('odt/' + filename + '.odt')
    list = []
    for i in odt.body:
        list.append(i.plaintext())
    return '\n'.join(list)


def write_bytes_to_file(bytes, f):
    line = ""
    for ch in bytes:
        if ch == '\n':
            if '??' not in line:
                f.write(line)
            line = ''
        else:
            line += ch


def compute(directory, foo):
    for i in main.get_files_name(directory):
        args = 'mystem/mystem.exe -n -w -l -d'
        proc = subprocess.Popen(
            args,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        res = proc.communicate(input=foo(i).encode())
        f = open('results/mystem/' + i + '.txt', 'w', encoding='utf-8')
        write_bytes_to_file(res[0].decode(), f)
        f.close()
        print(i + ' ready')

if __name__ == '__main__':
    compute('odt', getODTText)
    compute('docx', getText)



