import csv
import os
import subprocess
from abc import ABC, abstractmethod

import piexif

from api.convert import convert_to_exif_tool_data, convert_getter


class Operation(ABC):
    @abstractmethod
    def do(self):
        raise NotImplementedError


class ExifToolOperation(Operation):

    def __init__(self, name: str, type_file: str, file_path: str, output_dir: str, exif_data: dict[str, str]):
        self.file_path = file_path
        self.output_dir = output_dir
        self.exif_data = exif_data
        self.name = name
        self.type_file = type_file

    def do(self):
        output_file_path = os.path.join(self.output_dir, self.name + '.' + self.type_file)
        print("Output file path: {}".format(output_file_path))
        command = [r"F:/Downloads/exiftool-13.02_64/exiftool.exe"]
        for k, v in self.exif_data.items():
            add_f = f"{k}=" + v
            print(add_f)
            command.append(add_f)
        if self.type_file == "jpg":
            command.append(f"-EXIF:UserComment=Hello comm")
            command.append("-Rating=" + str(2))
        command.append("-o")
        command.append(output_file_path)
        command.append(self.file_path)
        subprocess.run(command)
        print(f"Метаданные обновлены. Новый файл сохранен как {output_file_path}")


class ExcelOperationExif(Operation):
    def __init__(self, file_path: str):
        self.file_path = file_path

    def do(self):
        data_list = []
        with open(self.file_path, mode='r', encoding='utf-8') as csv_file:
            csv_reader = csv.DictReader(csv_file, fieldnames=["A", "B", "C", "D", "E", "F", "G"])
            next(csv_reader, None)
            for row in csv_reader:
                data_list.append(
                    {"filename": row["A"], "path": row["B"], "type": row["C"], "name": row['D'], "title": row['E'],
                     "description": row['F'], "keywords": row['G'], })
        print(data_list)
        return data_list


class ExifOperationExif(Operation):
    def __init__(self, csv_path: str):
        self.csv_path = csv_path

    def do(self):
        result = ExcelOperationExif(self.csv_path).do()
        for res in result:
            types = res["type"].split(';')
            for t in types:
                print('Type: {}'.format(t))
                input_file = os.path.join(res['path'], f"{res['filename']}.{t}")
                if os.path.isfile(input_file):
                    exif_data = {
                        piexif.ImageIFD.XPTitle: res['title'],
                        piexif.ImageIFD.ImageDescription: res['description'],
                        piexif.ImageIFD.XPKeywords: res['keywords'],
                    }
                    conv = convert_getter[t]()
                    print(conv)
                    ExifToolOperation(res['name'], t, input_file, res['path'],
                                      convert_to_exif_tool_data(exif_data, conv)).do()
                else:
                    print("Not found exif file: in ", input_file)
