#!/usr/bin/python
# -*- coding: UTF-8 -*-

import xml.etree.ElementTree as ET

tree = ET.parse('testTV/True Detective.S02E08.Bluray.1080p.DTS-HD.MA.5.1.x265.10bit-CHD.nfo')
root = tree.getroot()

for element in root.iter('Data'):
    out = []
    for n in range(len(element)):
        out.append('{0}'.format(element[n].text))
    print(out)
