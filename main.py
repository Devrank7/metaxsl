import os

from dotenv import load_dotenv

from api.api import ExifOperationExif

load_dotenv()
SCRIPT_NAME = os.getenv("SCRIPT_NAME")
CSV_FILE_PATH = os.getenv("CSV_FILE_PATH")
EXIFTOOL = os.getenv("EXIFTOOL_PATH")


def main():
    print("Script name: {}".format(SCRIPT_NAME))
    if CSV_FILE_PATH is None or EXIFTOOL is None:
        print("Please set environment variables 'CSV_FILE_PATH' and 'EXIFTOOL'")
        return
    if not os.path.exists(CSV_FILE_PATH):
        print("CSV_FILE_PATH does not exist")
        return
    if not os.path.exists(EXIFTOOL):
        print("EXIFTOOL does not exist")
        return
    print("Exiftool = ", EXIFTOOL)
    print("Script Started")
    # exiftool = r"F:/Downloads/exiftool-13.02_64/exiftool.exe"
    ExifOperationExif(EXIFTOOL, CSV_FILE_PATH).do()


if __name__ == '__main__':
    main()
