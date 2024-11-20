# '  <option key="User" value="a_oividutov" />'
# '  <option key="User" value="master" />'
# '  <option key="User" value="user" />'
# '  <option key="Auth" value="C:GSb+0BRYhy%3EM[ln%7:HSkry+CHQavE" />'

import os
import chardet

dir_nxs = r'res/'
ext_nxs = '.nxs'
flag_edit_file = False
sample1 = '  <option key="User" value="a_oividutov" />'


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


# переход в папку для файлов
os.chdir(os.path.join(os.path.dirname(os.path.realpath(__file__)), dir_nxs))

# обрабатываются файлы по списку из папки
for full_name_nxs_file in get_files_nxs():
    # флаг нужности редактирования файла
    flag_edit_file = False

    # читаю файл в список
    with open(full_name_nxs_file, encoding=get_codepage(full_name_nxs_file)) as nxs_file:
        # НЕ сохраняя символы в конце строки и переносы
        list_each_string_of_file = nxs_file.read().splitlines()

        # # сохраняя символы в конце строки и переносы
        # list_each_string_of_file = nxs_file.readlines()

    # ищу строку с логинами a_oividutov или master
    for each_string in list_each_string_of_file:
        if sample1 == each_string:
            print(full_name_nxs_file, each_string)

# print()
# print(*list_each_string_of_file, end='\n', sep='\n')

# заменяю строку логина на user, а предыдущую на пароль от user

# end

# with open(filename, 'r') as file_html:
#     all_strings_file = file_html.read()

# with open(filename.text(), 'r') as file_html:
#     list_each_string_of_file = file_html.read().splitlines()
