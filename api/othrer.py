import os

import piexif
from PIL import Image

from .api import Operation


class ImgOperationExif(Operation):

    def __init__(self, name: str, type_file: str, file_path: str, output_dir: str, exif_data: dict[int, str]):
        self.file_path = file_path
        self.output_dir = output_dir
        self.exif_data = exif_data
        self.name = name
        self.type_file = type_file

    def do(self):
        image = Image.open(self.file_path)
        exif_dict = piexif.load(image.info.get("exif", b""))
        for key, val in self.exif_data.items():
            exif_dict["0th"][key] = val.encode("utf-8")
        exif_bytes = piexif.dump(exif_dict)
        new_file_name = self.name + '.' + self.file_path.split('.')[-1]
        os.makedirs(self.output_dir, exist_ok=True)
        new_file_path = os.path.join(self.output_dir, new_file_name)
        image.save(new_file_path, "jpeg", exif=exif_bytes)
        print(f"Автор обновлен. Новый файл сохранен как {new_file_path}")