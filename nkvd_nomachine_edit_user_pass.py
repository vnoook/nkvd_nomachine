# <option key="Auth" value="OSn+Fy.Ml#?]s1Of$BPr4D_w@Si&amp;K]t4VQ" />
# <option key="User" value="user" />
# PASS = '  <option key="Auth" value="OSn+Fy.Ml#?]s1Of$BPr4D_w@Si&amp;K]t4VQ" />\n'
# KEY1 = '  <option key="User" value="a_oividutov" />\n'
# KEY2 = '  <option key="User" value="master" />\n'
# RES = '  <option key="User" value="user" />\n'

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


# # чтение построчно файла
# with open(full_name_nxs_file, encoding='cp1251', newline='') as nxs_file:
#     row_csv_content = csv.reader(csvfile, delimiter=';')

# with open(filename, 'r') as file_html:
#     all_strings_file = file_html.read()

# with open(filename.text(), 'r') as file_html:
#     list_each_string_of_file = file_html.read().splitlines()

# end
