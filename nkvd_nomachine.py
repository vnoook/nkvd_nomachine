# в файле nxs нужно найти строку "Server host" в группе "General"
# например, группа <group name="General" > и строка "<option key="Server host" value="172.16.40.30" />"
#                  <group name = "Login" >           <option key="Auth"  value="++++++++++++" />
#                  <group name = "Login" >           <option key ="User" value = "user" / >

import os
import xml.etree.ElementTree as ET
import openpyxl

dir_nxs = r'res/'
ext_nxs = '.nxs'
file_xlsx = 'test1.xlsx'
dict_data_nxs_files = {}
dict_data_nxs_files_good_names = {}


def get_files_nxs(dir_nxs: str) -> list:
    list_of_files = None
    for data_of_scan in os.scandir():
        # если это файл и расширение, то из этого файла берутся данные
        if data_of_scan.is_file() and os.path.splitext(os.path.split(data_of_scan)[1])[1] == ext_nxs:
            if not list_of_files:
                print(full_path_file, full_name_file)
                full_path_file = data_of_scan.path
                full_name_file = data_of_scan.name
                list_of_files.append()
            else:
                list_of_files = []


# функция чтения файла nxs, формат xml
def get_ip_from_nxs(file: str) -> list:
    """
    Функция чтения файла nxs (формат xml)
    берёт из файла поле "Server host"
    выдаёт кортеж - файл в котором ищется и ИП-адрес подключения
    """

    tree = ET.parse(file)
    root = tree.getroot()
    rez = None

    # чтение всех атрибутов в дереве по-очереди
    # поиск значений адреса "General-Server host" первым
    for branch in root:
        if branch.attrib['name'] == 'General':
            for sub_branch in branch:
                key = sub_branch.attrib.get('key')
                val = sub_branch.attrib.get('value')
                if key == 'Server host':
                    rez = [file, val]

    # поиск значений адреса "Login-User" вторым
    for branch in root:
        if branch.attrib['name'] == 'Login':
            for sub_branch in branch:
                key = sub_branch.attrib.get('key')
                val = sub_branch.attrib.get('value')
                if key == 'User':
                    rez.append(val)

    # поиск значений адреса "Login-Auth" третьим
    for branch in root:
        if branch.attrib['name'] == 'Login':
            for sub_branch in branch:
                key = sub_branch.attrib.get('key')
                val = sub_branch.attrib.get('value')
                if key == 'Auth':
                    rez.append(val)

    return rez


# функция извлечения из имени файла подстроки до символа "("
def spliter_name(string_name: str) -> str:
    return string_name.rsplit('(', 1)[0]


# создаётся эксель
wb = openpyxl.Workbook()
wb_s = wb.active
wb_s.append(['IP', 'NAME'])

# переход в папку для файлов и поиск в ней файлов
# создание двух словарей - реальные файлы и файлы с нужными названиями для слияний
os.chdir(os.path.join(os.path.dirname(os.path.realpath(__file__)), dir_nxs))

print(get_files_nxs(dir_nxs))
exit()

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
            # if 'Подключение' not in full_name_file:
            dict_data_nxs_files[ip_addr].append(full_name_file)

        # создание и добавление в словарь списка уже подготовленных коротких имён
        if dict_data_nxs_files_good_names.get(ip_addr) is None:
            dict_data_nxs_files_good_names[ip_addr] = {short_name_file}
        else:
            # if 'Подключение' not in short_name_file:
            dict_data_nxs_files_good_names[ip_addr].add(short_name_file)

        wb_s.append([ip_addr, short_name_file])

os.chdir(os.path.dirname(os.path.realpath(__file__)))
wb.save(file_xlsx)
wb.close()

print()
os.chdir(os.path.join(os.path.dirname(os.path.realpath(__file__)), dir_nxs))
for key_ip, val_names in dict_data_nxs_files.items():
    new_name = ' '.join(dict_data_nxs_files_good_names[key_ip]).strip()+'_.nxs'
    print(val_names)
    if len(val_names) > 1:
        for real_file in val_names:
            if val_names.index(real_file) == 0:
                print('переименовываю "'+real_file+'" в "'+new_name+'"')
                # os.rename(real_file, new_name)
            else:
                print('удаляю', real_file)
                # os.remove(real_file)
        print()
