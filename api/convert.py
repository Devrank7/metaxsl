from abc import ABC, abstractmethod

import piexif


class ConvertFiler(ABC):
    def convert(self, key):
        return self.data().get(key)

    @abstractmethod
    def data(self) -> dict[str, str]:
        raise NotImplementedError


class JPGConvertFilter(ConvertFiler):

    def data(self) -> dict[str, str]:
        return {
            piexif.ImageIFD.ImageDescription: "-EXIF:ImageDescription",
            piexif.ImageIFD.XPTitle: "-XMP:Title",
            piexif.ImageIFD.XPKeywords: "-XMP:Subject",
        }


class EPSConvertFilter(ConvertFiler):
    def data(self) -> dict[str, str]:
        return {
            piexif.ImageIFD.ImageDescription: "-Copyright",
            piexif.ImageIFD.XPTitle: "-Title",
            piexif.ImageIFD.XPKeywords: "-Keywords",
        }


convert_getter = {
    "jpg": JPGConvertFilter,
    "eps": EPSConvertFilter,
}


def convert_to_exif_tool_data(exif_data: dict[int, str], convert_type: ConvertFiler) -> dict[str, str]:
    new_exif_data: dict[str, str] = {}
    for k, v in exif_data.items():
        new_exif_data[convert_type.convert(k)] = v
    return new_exif_data
