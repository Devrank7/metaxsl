import os
import uuid

import piexif
from PIL import Image

from api.image import ExcelOperationExif


def update_jpeg_author(file_path, output_dir: str, exif_data: dict[int, str]):
    image = Image.open(file_path)
    exif_dict = piexif.load(image.info.get("exif", b""))
    for key, val in exif_data.items():
        exif_dict["0th"][key] = val.encode("utf-8")
    exif_bytes = piexif.dump(exif_dict)
    new_file_name = f"updated_{uuid.uuid4().hex}" + file_path.split('/')[-1]
    os.makedirs(output_dir, exist_ok=True)
    new_file_path = os.path.join(output_dir, new_file_name)
    image.save(new_file_path, "jpeg", exif=exif_bytes)
    print(f"Автор обновлен. Новый файл сохранен как {new_file_path}")


def main():
    exif_data = {
        piexif.ImageIFD.Artist: "Tony",
        piexif.ImageIFD.ImageDescription: "SOME DESCRIPTION",
    }
    ExcelOperationExif(r'F:/Downloads/ugggggg.csv').do()
    # update_jpeg_author(r"F:/Downloads/hippocrite-funny-cartoon-pun-animal-hypocrisy/yzf2_fmia_231108.jpg",
    #                   r"F:/Downloads/hippocrite-funny-cartoon-pun-animal-hypocrisy",
    #                   exif_data)


if __name__ == '__main__':
    main()
