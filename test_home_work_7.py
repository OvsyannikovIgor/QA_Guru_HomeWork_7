import os
import shutil
import zipfile

from script_os import CURRENT_DIR


def test_home_work_7():
    if not os.path.exists("resource"):
        os.mkdir("resource")
    with zipfile.ZipFile('resource/HomeWork.zip', mode='a', compression=zipfile.ZIP_DEFLATED,
                         compresslevel=5) as zip_file:
        print('Zip создан:', zip_file.namelist())
        zip_file.write('tmp/file_example_XLSX_50.xlsx')
        zip_file.write('tmp/Python Testing with Pytest (Brian Okken).pdf')
        print('Добавил файлы:', zip_file.namelist())
        pass
