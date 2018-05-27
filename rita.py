import subprocess
import xml.etree.cElementTree as ET

from ie import marks


def readXML(fulldoc, listoffacts):
    tomita_names = []
    while True:
        try:
            element = next(fulldoc)
            filename = element.attrib['url'].replace("\\", '')
            facts = element.iter(listoffacts[0])
            while True:
                try:
                    tag = next(facts)
                    names = tag.iter(listoffacts[1])
                    while True:
                        try:
                            tomita_names.append(filename.lower() + " " + next(names).attrib['val'].lower())
                        except StopIteration:
                            break
                except StopIteration:
                    break
        except StopIteration:
            break
    return tomita_names

if __name__ == '__main__':
    args = 'tomita/tomitaparser.exe tomita/config.proto'
    proc = subprocess.Popen(
            args,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
    res = proc.communicate()
    xml = res[0].decode()
    print("finish tomita work")
    tree = ET.XML(xml)
    doc = tree.iter("document")
    tomita_names = readXML(doc, ["Names", "Name"])
    marks.countF(tomita_names, "Томита-парсер")
    for c in tomita_names:
        print("{0} {1}".format(c, marks.right_names[tomita_names.index(c)]))








