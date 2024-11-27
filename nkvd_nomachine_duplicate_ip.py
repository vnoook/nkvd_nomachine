# в файле nxs нужно найти строку "Server host" в группе "General"
# например, группа <group name="General" > и строка "<option key="Server host" value="172.16.40.30" />"

import os
import xml.etree.ElementTree as ET

dir_nxs = r'res/'
ext_nxs = '.nxs'
list_of_nxs_files = []
dict_of_nxs_files = {}


# получение файлов с расширением из текущей папки
def get_files_nxs() -> list:
    list_of_files = None
    for data_of_scan in os.scandir():
        # если это файл и расширение, то из этого файла берутся данные
        if data_of_scan.is_file() and os.path.splitext(os.path.split(data_of_scan)[1])[1] == ext_nxs:
            filename = data_of_scan.name
            if list_of_files is None:
                list_of_files = [filename]
            else:
                list_of_files.append(filename)
    return list_of_files


# функция получения ip адреса из файла nxs, формат xml
def get_ip_from_nxs(file: str) -> list:
    """
    Функция чтения файла nxs (формат xml)
    берёт из файла поле "Server host"
    выдаёт кортеж - файл в котором ищется и ИП-адрес подключения
    """

    tree = ET.parse(file)
    root = tree.getroot()
    rez = 0

    # чтение всех атрибутов в дереве по-очереди
    # поиск значений адреса "General-Server host" первым
    for branch in root:
        if branch.attrib['name'] == 'General':
            for sub_branch in branch:
                key = sub_branch.attrib.get('key')
                val = sub_branch.attrib.get('value')
                if key == 'Server host':
                    rez = [file, val]
    return rez


# переход в папку для файлов и поиск в ней файлов
os.chdir(os.path.join(os.path.dirname(os.path.realpath(__file__)), dir_nxs))

# получение списка файлов nxs в текущей папке
list_of_nxs_files = get_files_nxs()

# если в папке есть файлы, то искать в них адрес и считать их количество, чтобы найти дублированные
if not list_of_nxs_files:
    print()
    print('файлы nxs в папке не найдены')
else:
    for full_name_file in list_of_nxs_files:
        ip_addr = get_ip_from_nxs(full_name_file)[1].strip()

        if dict_of_nxs_files.get(ip_addr):
            temp_list = dict_of_nxs_files[ip_addr]
            temp_list.append(full_name_file)
            dict_of_nxs_files[ip_addr] = temp_list
        else:
            dict_of_nxs_files[ip_addr] = [full_name_file]

for k,v in dict_of_nxs_files.items():
    if v:
        if len(v) > 1:
            print(k, v, sep=' ... ')
