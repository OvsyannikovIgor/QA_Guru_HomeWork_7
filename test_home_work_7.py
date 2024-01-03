import csv
import os
import shutil
import zipfile
from io import TextIOWrapper
from zipfile import ZipFile

import pytest
from openpyxl import load_workbook
from pypdf import PdfReader

from script_os import CURRENT_DIR


@pytest.fixture(scope='function')
def delete_resource():
    if os.path.exists("resource") is True:
        shutil.rmtree(os.path.join(CURRENT_DIR, "resource"))


def test_create_zip_file(delete_resource):
    if not os.path.exists("resource"):
        os.mkdir("resource")
    with zipfile.ZipFile('resource/HomeWork.zip', mode='a', compression=zipfile.ZIP_DEFLATED,
                         compresslevel=5) as zip_file:
        zip_file.write('tmp/file_example_XLSX_50.xlsx')
        zip_file.write('tmp/Python Testing with Pytest (Brian Okken).pdf')
        zip_file.write('tmp/scenario_export_1454558.csv')
        assert zip_file.namelist() == ['tmp/file_example_XLSX_50.xlsx',
                                       'tmp/Python Testing with Pytest (Brian Okken).pdf',
                                       'tmp/scenario_export_1454558.csv'], 'Список не соответствует ожиданию'


def test_check_xlsx_file():
    with ZipFile('resource/HomeWork.zip') as zip_file:
        assert zip_file.namelist()[0] == 'tmp/file_example_XLSX_50.xlsx', 'xlsx файл в zip не найден'
        file = PdfReader(zip_file.namelist()[1])
        assert len(file.pages) == 256, 'кол-во страниц не совпадает'
        assert '2.Learn pytest While Testing an Example Application' in file.pages[3].extract_text(), \
            'Ожидаемый текст в pdf файле не найден'


def test_check_pdf_file():
    with ZipFile('resource/HomeWork.zip') as zip_file:
        assert zip_file.namelist()[1] == 'tmp/Python Testing with Pytest (Brian Okken).pdf', 'pdf файл в zip не найден'
        file = load_workbook(zip_file.namelist()[0])
        sheet = file.active
        assert sheet['B1'].value == 'First Name'
        assert sheet['C1'].value == 'Last Name'


def test_check_csv_file():
    with ZipFile('resource/HomeWork.zip') as zip_file:
        assert zip_file.namelist()[2] == 'tmp/scenario_export_1454558.csv', 'csv файл в zip не найден'
        with zip_file.open(zip_file.namelist()[2], "r") as csv_file:
            csv_reader = list(csv.reader(TextIOWrapper(csv_file, 'utf-8')))
            assert csv_reader.__len__() == 223, 'Количество строк в файле не совпадает'
            assert '\ufeff0;Состояние;"Комната открыта"' in csv_reader[0], \
                'Ожидаемый текст в csv файле не найден'
