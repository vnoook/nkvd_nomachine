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
def get_codepage(one_file: str):
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
    flag_edited = False

    for branch in root:
        if branch.attrib['name'] == 'Login':
            for sub_branch in branch:
                key = sub_branch.attrib.get('key')
                if key == 'User':
                    sub_branch.set('value', 'user')
                    # sub_branch.attrib['value'] = '222'
                    flag_edited = True
                if key == 'Auth':
                    sub_branch.set('value', r"-gZPFTA;5#upbTOA80urkULA@0zqp]OFE/")
                    flag_edited = True

                if flag_edited:
                    tree.write(file)
                    line_prepender(file)


def line_prepender(filename: str):
    doctype = '<!DOCTYPE NXClientSettings>'
    with open(filename, 'r+') as f:
        content = f.read()
        f.seek(0, 0)
        f.write(doctype.rstrip('\r\n') + '\n' + content)


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
        edit_userpass_nxs(k[0])
        print('обработан файл - ', k[0])
