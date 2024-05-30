# в файле nxs нужно найти строку "Server host" в группе "General"
# например, группа <group name="General" > и строка "<option key="Server host" value="172.16.40.30" />"

import xml.etree.ElementTree as ET
import openpyxl

file_nxs = 'res/test1.nxs'
file_xlsx = 'test1.xlsx'

# wb = openpyxl.Workbook()
# wb_s = wb.active
# wb_s.append(["IP", "Name"])

tree = ET.parse(file_nxs)
root = tree.getroot()

# чтение конкретного атрибута
# print(root[0][1].attrib)
print()

# # чтение всех атрибутов в дереве
# for branch in root:
#     print(f'{branch.tag = } ... {branch.attrib = }')
#     for sub_branch in branch:
#         print(f'... {sub_branch.tag = } ... {sub_branch.attrib = }')
#         # if sub_branch.attrib.get['Server host']:
#         #     print('!!!!!!!!')
# print()

# чтение всех атрибутов в дереве
for branch in root:
    if branch.attrib['name'] == 'General':
        for sub_branch in branch:
            if sub_branch.attrib['key'] == 'Server host':
                print(f'{branch.tag = } ... {branch.attrib = }')
                print(f'... {sub_branch.tag = } ... {sub_branch.attrib = }')
                # if sub_branch.attrib.get['Server host']:
                #     print('!!!!!!!!')
print()


# for branch in root:
#     if branch.attrib['name'] == 'General':
#         # print(f'{branch.tag = } ... {branch.attrib = }')
#         print(f'{root[0][1].attrib = }')
#         print(root[0][1].attrib)

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
