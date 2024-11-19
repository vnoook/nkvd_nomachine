# '  <option key="User" value="a_oividutov" />'
# '  <option key="User" value="master" />'
# '  <option key="User" value="user" />'
# '  <option key="Auth" value="C:GSb+0BRYhy%3EM[ln%7:HSkry+CHQavE" />'

import os
import chardet

dir_nxs = r'res/'
ext_nxs = '.nxs'
flag_edit_file = False


# получение файлов с расширением из папки
def get_files_nxs() -> list:
    list_of_files = None
    for data_of_scan in os.scandir():
        # если это файл и расширение nxs, то этот файл добавляется в список
        if data_of_scan.is_file() and os.path.splitext(os.path.split(data_of_scan)[1])[1] == ext_nxs:
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


# переход в папку для файлов
os.chdir(os.path.join(os.path.dirname(os.path.realpath(__file__)), dir_nxs))
# и поиск в ней файлов
for full_name_nxs_file in get_files_nxs():
    print(full_name_nxs_file, ',', get_codepage(full_name_nxs_file))
    flag_edit_file = False

    # читаю файл построчно, ищу строку с логинами a_oividutov или master
    # заменяю строку логина на user, а предыдущую на пароль от user
    with open(full_name_nxs_file, encoding=get_codepage(full_name_nxs_file)) as nxs_file:
        list_each_string_of_file = nxs_file.read().splitlines()

    print(list_each_string_of_file)
    exit()

# end

# with open(filename, 'r') as file_html:
#     all_strings_file = file_html.read()

# with open(filename.text(), 'r') as file_html:
#     list_each_string_of_file = file_html.read().splitlines()
