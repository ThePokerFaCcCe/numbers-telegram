from pathlib import Path
import xlsxwriter
from datetime import datetime


class Excel:
    dir_path: Path = Path().cwd()/"export"
    __file_path: Path
    _workbook: xlsxwriter.Workbook
    _worksheet: xlsxwriter.workbook.Worksheet

    def __create_filename(self):
        """Return string based on `datetime.now()`"""
        return datetime.now().strftime("%y-%m-%dT%H-%M-%S")

    def __init__(self, filename=None, ext='.xlsx'):
        """
        Create an excel file with `filename` inside of `self.dir_path`
        """
        filename = f"{filename or self.__create_filename()}{ext}"
        self.__file_path = self.dir_path/filename
        self._workbook = xlsxwriter.Workbook(self.file_path)
        self._worksheet = self._workbook.add_worksheet()

    @property
    def worksheet(self):
        """Return worksheet that can be used for writing data"""
        return self._worksheet

    @property
    def file_path(self):
        return self.__file_path

    def close(self):
        """Close file"""
        self.dir_path.mkdir(exist_ok=True)
        self._workbook.close()
