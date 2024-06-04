# в файле nxs нужно найти строку "Server host" в группе "General"
# например, группа <group name="General" > и строка "<option key="Server host" value="172.16.40.30" />"

import os
import xml.etree.ElementTree as ET
import openpyxl

def get_ip_from_nxs(file_nxs):
    tree = ET.parse(file_nxs)
    root = tree.getroot()
    rez = None

    # чтение всех атрибутов в дереве по-очереди
    for branch in root:
        if branch.attrib['name'] == 'General':
            for sub_branch in branch:
                key = sub_branch.attrib.get('key')
                val = sub_branch.attrib.get('value')
                if (key == 'Server host') and val:
                    rez = (file_nxs, sub_branch.attrib.get('value'))
    print(rez)
    return rez

file_nxs = 'res/test1.nxs'
file_xlsx = 'test1.xlsx'
get_ip_from_nxs('res/test1.nxs')
etx_nxs = '.nxs'
# print(get_ip_from_nxs('res/test1.nxs'))
# print(type(get_ip_from_nxs(file_nxs)))

for data_of_scan in os.scandir():
    if data_of_scan.is_file() and os.path.splitext(os.path.split(data_of_scan)[1])[1] == etx_nxs:
        print(data_of_scan)
        # os.remove(data_of_scan)

# wb = openpyxl.Workbook()
# wb_s = wb.active
# wb_s.append(["IP", "Name"])

# wb.save(file_xlsx)
# wb.close()
