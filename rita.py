import subprocess
import xml.etree.cElementTree as ET


args = 'tomita/tomitaparser.exe tomita/config.proto'
proc = subprocess.Popen(
            args,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
res = proc.communicate()
xml = res[0].decode()
tree = ET.XML(xml)
doc = tree.iter("document")
tomita_names = {}
while True:
    try:
        element = next(doc)
        filename = element.attrib['url'].replace("\\", '')
        current = []
        facts = element.iter("Names")
        while True:
            try:
                tag = next(facts)
                names = tag.iter("Name")
                while True:
                    try:
                        current.append(next(names).attrib['val'])
                    except StopIteration:
                        break
            except StopIteration:
                break
        tomita_names[filename] = current
    except StopIteration:
        break




