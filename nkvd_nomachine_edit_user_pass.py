# '  <option key="User" value="a_oividutov" />'
# '  <option key="User" value="master" />'
# '  <option key="User" value="user" />'
# '  <option key="Auth" value="C:GSb+0BRYhy%3EM[ln%7:HSkry+CHQavE" />'

import os
import chardet
import xml.etree.ElementTree as ET


dir_nxs = r'res/'
ext_nxs = '.nxs'
reserved_users = ('user', 'pi', 'adminsec', 'video')
list_files_with_attr = []


# получение файлов с расширением из текущей папки
def get_files_nxs() -> list:
    list_of_files = None
    for data_of_scan in os.scandir():
        # расширение файла
        ext_file = os.path.splitext(os.path.split(data_of_scan)[1])[1]
        # если это файл и нужное расширение, то этот файл добавляется в список
        if data_of_scan.is_file() and ext_file == ext_nxs:
            full_name = data_of_scan.name
            if list_of_files is None:
                list_of_files = []
            else:
                list_of_files.append(full_name)
    return list_of_files


# получение кодировки файла
def get_codepage(one_file):
    detector = chardet.universaldetector.UniversalDetector()
    with open(one_file, 'rb') as fh:
        for line in fh:
            detector.feed(line)
            if detector.done:
                break
        detector.close()
    return detector.result['encoding']


# чтение некоторых атрибутов из файла nxs, формат xml
def get_userpass_from_nxs(file: str) -> list:
    """
    Функция чтения файла nxs (формат xml)
    """
    tree = ET.parse(file)
    root = tree.getroot()
    rez = None

    # чтение всех атрибутов в дереве по-очереди
    # поиск значений адреса "Login-User" вторым
    for branch in root:
        if branch.attrib['name'] == 'Login':
            for sub_branch in branch:
                key = sub_branch.attrib.get('key')
                val = sub_branch.attrib.get('value')
                if key == 'User':
                    rez = [file, val]

    # поиск значений адреса "Login-Auth" третьим
    for branch in root:
        if branch.attrib['name'] == 'Login':
            for sub_branch in branch:
                key = sub_branch.attrib.get('key')
                val = sub_branch.attrib.get('value')
                if key == 'Auth':
                    rez.append(val)

    return rez


# редактирование атрибутов файла nxs, формат xml
def edit_userpass_nxs(file: str):
    tree = ET.parse(file)
    root = tree.getroot()

    for elem in root.iter('User'):
        print()
        print(elem)
        print(elem.text)
        print(elem.attrib)
        print(elem.keys())

        elem.set('User', '111')
        elem.text = 'new_text'
    tree.write(file)

    # for elem in root.iter('tag_name'):
    #     elem.set('attribute_name', 'new_value')
    #     elem.text = 'new_text'

    # for rank in root.iter('Login'):
    #     rank.text = str(new_rank)
    #     rank.set('updated', 'yes')
    # tree.write(file)


# переход в папку для файлов
os.chdir(os.path.join(os.path.dirname(os.path.realpath(__file__)), dir_nxs))

# получение списка файлов nxs в папке
list_of_nxs_files = get_files_nxs()

# обрабатываются файлы по списку из папки и формируется список списков
for full_name_nxs_file in list_of_nxs_files:
    list_files_with_attr.append(get_userpass_from_nxs(full_name_nxs_file))

for k in list_files_with_attr:
    if k[1] not in reserved_users:
        # print(k[1], ' ....... ', k[0])
        pass

edit_userpass_nxs('131.nxs')

# with open(filename, 'r') as file_html:
#     all_strings_file = file_html.read()

# with open(filename.text(), 'r') as file_html:
#     list_each_string_of_file = file_html.read().splitlines()

# # читаю файл в список
# with open(full_name_nxs_file, encoding=get_codepage(full_name_nxs_file)) as nxs_file:
#     # НЕ сохраняя символы конца строки
#     list_each_string_of_file = nxs_file.read().splitlines()
#     # # сохраняя символы конца строки
#     # list_each_string_of_file = nxs_file.readlines()
