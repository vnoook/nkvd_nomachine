# в файле nxs нужно найти строку "Server host" в группе "General"
# например, группа <group name="General" > и строка "<option key="Server host" value="172.16.40.30" />"

import os
import xml.etree.ElementTree as ET
import openpyxl


# функция чтения файла nxs, формат xml
def get_ip_from_nxs(file: str) -> tuple:
    """
    функция чтения файла nxs (формат xml)
    берёт из файла поле "Server host"
    выдаёт кортеж - файл в котором ищется и ИП-адрес подключения
    """

    tree = ET.parse(file)
    root = tree.getroot()
    rez = None

    # чтение всех атрибутов в дереве по-очереди
    for branch in root:
        if branch.attrib['name'] == 'General':
            for sub_branch in branch:
                key = sub_branch.attrib.get('key')
                val = sub_branch.attrib.get('value')
                if (key == 'Server host') and val:
                    rez = (file, sub_branch.attrib.get('value'))
    return rez


file_nxs = 'res/test1.nxs'
dir_nxs = r'res/'
file_xlsx = 'test1.xlsx'
get_ip_from_nxs('res/test1.nxs')
etx_nxs = '.nxs'

wb = openpyxl.Workbook()
wb_s = wb.active
wb_s.append(['IP', 'NAME'])

os.chdir(os.path.join(os.path.dirname(os.path.realpath(__file__)), dir_nxs))
for data_of_scan in os.scandir():
    if data_of_scan.is_file() and os.path.splitext(os.path.split(data_of_scan)[1])[1] == etx_nxs:
        wb_s.append([get_ip_from_nxs(data_of_scan.name)[1], get_ip_from_nxs(data_of_scan.name)[0]])

os.chdir(os.path.dirname(os.path.realpath(__file__)))
wb.save(file_xlsx)
wb.close()
