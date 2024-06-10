# в файле nxs нужно найти строку "Server host" в группе "General"
# например, группа <group name="General" > и строка "<option key="Server host" value="172.16.40.30" />"

import os
import xml.etree.ElementTree as ET
import openpyxl
# import difflib

dir_nxs = r'res/'
ext_nxs = '.nxs'
file_xlsx = 'test1.xlsx'
dict_data_nxs_files = {}
dict_data_nxs_files_good_names = {}


# функция чтения файла nxs, формат xml
def get_ip_from_nxs(file: str) -> tuple:
    """
    Функция чтения файла nxs (формат xml)
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


# функция извлечения из имени файла подстроки до символа "("
def spliter_name(string_name: str) -> str:
    # print(string_name, '===', string_name.split('(', 1), '===', string_name.split('(', 1)[0])
    return string_name.split('(', 1)[0]


# создаётся эксель
wb = openpyxl.Workbook()
wb_s = wb.active
wb_s.append(['IP', 'NAME'])

# переход в папку для файлов и поиск в ней файлов
# создание двух словарей - реальные файлы и файлы с нужными названиями для слияний
os.chdir(os.path.join(os.path.dirname(os.path.realpath(__file__)), dir_nxs))
for data_of_scan in os.scandir():
    # если это файл и расширение, то из этого файла берутся данные
    if data_of_scan.is_file() and os.path.splitext(os.path.split(data_of_scan)[1])[1] == ext_nxs:
        # подготовка переменных
        ip_addr = get_ip_from_nxs(data_of_scan.name)[1].strip()
        full_path_file = data_of_scan.path
        full_name_file = data_of_scan.name
        name_file = os.path.splitext(os.path.split(full_name_file)[1])[0]
        short_name_file = spliter_name(name_file)





        # создание словаря с реальными файлами
        if dict_data_nxs_files.get(ip_addr) is None:
            dict_data_nxs_files[ip_addr] = [full_name_file]
        else:
            if 'Подключение' not in full_name_file:
                dict_data_nxs_files[ip_addr].append(full_name_file)



        # создание и добавление в словарь списка уже подготовленных коротких имён
        if dict_data_nxs_files_good_names.get(ip_addr) is None:
            dict_data_nxs_files_good_names[ip_addr] = {short_name_file}
        else:
            if 'Подключение' not in short_name_file:
                dict_data_nxs_files_good_names[ip_addr].add(short_name_file)

        wb_s.append([ip_addr, short_name_file])

os.chdir(os.path.dirname(os.path.realpath(__file__)))
wb.save(file_xlsx)
wb.close()

# print()
# print(len(dict_data_nxs_files_good_names), dict_data_nxs_files_good_names)
# print(len(dict_data_nxs_files), dict_data_nxs_files)

# print()
# for key_ip, val_names in dict_data_nxs_files.items():
#     print(key_ip, val_names)
#     for name in val_names:
#         print(name)
#         # pass
#     print()

# print()
# for key_ip, val_names in dict_data_nxs_files_good_names.items():
#     print(key_ip, val_names)
#     for name in val_names:
#         print(name)
#         # pass
#     print()

print()
for key_ip, val_names in dict_data_nxs_files.items():
    new_name = ' '.join(dict_data_nxs_files_good_names[key_ip]).strip()
    print(key_ip)
    # print(dict_data_nxs_files[key_ip])
    print(dict_data_nxs_files_good_names[key_ip])
    print(new_name)
    print()




# # сравнение имён файлов между именем архива и именем csv файла, они должны почти совпадать
# diff_ratio_file_names = difflib.SequenceMatcher(
#     None,
#     take_file[2],
#     self.parse_file_parts(file_in_zf.filename)[2]).ratio()
# if diff_ratio_file_names < 0.9:
#     pass

# print(name_file)  # file path
# print(os.path.splitext(os.path.split(data_of_scan)[1]))  # file,ext
# print(os.path.splitext(os.path.split(data_of_scan)[1])[0])  # file
# print(os.path.splitext(os.path.split(data_of_scan)[1])[1])  # ext
# print()