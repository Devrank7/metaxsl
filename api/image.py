import csv
import os
import uuid
from abc import ABC, abstractmethod

import piexif
from PIL import Image


class Operation(ABC):
    @abstractmethod
    def do(self):
        raise NotImplementedError


class ImgOperationExif(Operation):

    def __init__(self, name: str,  file_path: str, output_dir: str, exif_data: dict[int, str]):
        self.file_path = file_path
        self.output_dir = output_dir
        self.exif_data = exif_data
        self.name = name

    def do(self):
        image = Image.open(self.file_path)
        exif_dict = piexif.load(image.info.get("exif", b""))
        for key, val in self.exif_data.items():
            exif_dict["0th"][key] = val.encode("utf-8")
        exif_bytes = piexif.dump(exif_dict)
        new_file_name = self.name + self.file_path.split('.')[-1]
        os.makedirs(self.output_dir, exist_ok=True)
        new_file_path = os.path.join(self.output_dir, new_file_name)
        image.save(new_file_path, "jpeg", exif=exif_bytes)
        print(f"Автор обновлен. Новый файл сохранен как {new_file_path}")


class EpsOperationExif(Operation):
    def __init__(self, file_path: str, output_dir: str, exif_data: dict[int, str]):
        self.file_path = file_path
        self.output_dir = output_dir
        self.exif_data = exif_data

    def do(self):
        pass


class ExcelOperationExif(Operation):
    d = {
        "filename": "Name",
        "path": "Path",
        "image": "Image",
        "name": "name",
        "title": "Title",
        "description": "Description",
        "keywords": "keywords",
    }

    def __init__(self, file_path: str):
        self.file_path = file_path

    def do(self):
        data_list = []
        with open(self.file_path, mode='r', encoding='utf-8') as csv_file:
            csv_reader = csv.DictReader(csv_file, fieldnames=["A", "B", "C"])
            next(csv_reader, None)
            for row in csv_reader:
                data_list.append({
                    "filename": row["A"],
                    "path": row["B"],
                    "type": row["C"]
                })
        print(data_list)
        return data_list


class ExifOperationExif(Operation):
    def __init__(self, csv_path: str):
        self.csv_path = csv_path

    def do(self):
        result = ExcelOperationExif(self.csv_path).do()
        for res in result:
            input_file = os.path.join(res['path'], f"{res['filename']}.{res['type']}")
            if os.path.isfile(input_file):
                exif_data = {
                    piexif.ImageIFD.XPTitle: res['title'],
                    piexif.ImageIFD.ImageDescription: res['description'],
                    piexif.ImageIFD.XPKeywords: res['keywords'],
                }
                ImgOperationExif(res['name'], input_file, res['path'], exif_data).do()
