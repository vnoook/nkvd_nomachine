# в файле nxs нужно найти строку "Server host" в группе "General"
# например, группа <group name="General" > и строка "<option key="Server host" value="172.16.40.30" />"

import xml.etree.ElementTree as ET
import openpyxl

file_nxs = 'res/test1.nxs'
file_xlsx = 'test1.xlsx'

# wb = openpyxl.Workbook()
# wb_s = wb.active
# wb_s.append(["IP", "Name"])

root_node = ET.parse(file_nxs).getroot()
# root_node = ET.parse('guid.xml').getroot()
# print(f'{root_node.tag = } ... {root_node.attrib = }')

for branch in root_node:
    if branch.attrib['name'] == 'General':
        print(f'{branch.tag = } ... {branch.attrib = }')
        print(f'{root_node[0][6].text = }')

# wb.save(file_xlsx)
# wb.close()

# print('Done')

# for tag in root_node.findall('Department'):
#     id_value = tag.get('ID')
#     if not id_value:
#         id_value = 'UNKNOWN DATA'
#         print(id_value)
#
#     name_value = tag.get('Name')
#     if not name_value:
#         name_value = 'UNKNOWN DATA'
#         print(name_value)
#
#     wb_s.append([id_value, name_value])
#
# wb.save(file_xlsx)
# wb.close()
