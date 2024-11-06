import os

from dotenv import load_dotenv

from api.api import ExifOperationExif

load_dotenv()
SCRIPT_NAME = os.getenv("SCRIPT_NAME")
CSV_FILE_PATH = os.getenv("CSV_FILE_PATH")


def main():
    print("Script name: {}".format(SCRIPT_NAME))
    ExifOperationExif(r'F:/Downloads/ugggggg.csv').do()


if __name__ == '__main__':
    main()
