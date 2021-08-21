import sys
import xml.etree.ElementTree as ET


def main(xml_file):
    root = ET.parse(xml_file).getroot()
    for child in root:
        print(child.tag)
        print(child.attrib)


if __name__ == '__main__':
    xml_file = sys.argv[1]
    xml_file = "test2.xml"
    main(xml_file)
