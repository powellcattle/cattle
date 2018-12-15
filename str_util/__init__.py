__author__ = 'spowell'
import datetime
import ftplib
import logging
import os
import socket
import zipfile


def sde_workspace():
    if socket.gethostname() == "gis-development":
        workspace = r"C:\\Users\\sde\\AppData\\Roaming\\ESRI\\" \
                    r"Desktop10.3\\ArcCatalog\\dev.cityofelcampo.org.sde"
    elif socket.gethostname() == "gis":
        workspace = r"C:\\Users\\spowell\\AppData\\Roaming\\ESRI\Desktop10.3\\" \
                    r"ArcCatalog\\powellcattle.com.sde"
    else:
        workspace = \
            r"C:\\Users\\spowell\\AppData\\Roaming\\ESRI\\" \
            r"Desktop10.3\\ArcCatalog\\black-charolais.com.sde"
    return workspace


def get_ftp_file(_site, _user, _password, _directory, _file_name):
    logging.info("Connecting to %s" % _site)
    try:
        ftp = ftplib.FTP(_site)
        ftp.login(_user, _password)

        ftp.cwd(_directory)
        file = open(_file_name, "wb")
        logging.info("Downloading %s from FTP site" % _file_name)
        ftp.retrbinary("RETR %s" % _file_name, (file.write))
        return

    except ftplib.all_errors as e:
        logging.error(e)
        return None
    finally:
        if file:
            file.close()
        ftp.quit()


def unzip_CAD(_path, _file_name):
    logging.info("unzip %s" % _file_name)
    fh = None
    outfile = None

    try:
        outfile = None
        cad_file = os.path.join(_path, _file_name)
        fh = open(cad_file, "rb")
        z = zipfile.ZipFile(fh)
        # path = os.path.join(_path, "junk")

        for name in z.namelist():
            # fname = os.path.join(path, name)
            outfile = open(name, "wb")
            outfile.write(z.read(name))
            outfile.close()
    except zipfile.error as e:
        logging.error(e)
    finally:
        if outfile:
            outfile.close()
        if fh:
            fh.close();


def concat_to_os_path(_path: str, _file: str) -> str:
    return os.path.join(_path, _file)


def to_pos_int_or_none(_str: str) -> int:
    try:
        integer = int(_str)
    except ValueError:
        return None
    else:
        return integer


def to_boolean_or_none(_str: str) -> bool:
    tf = None
    try:
        if _str.upper() == "TRUE":
            tf = True
        else:
            tf = False

    except ValueError:
        return None
    else:
        return tf


def to_pos_long_or_none(_str: str) -> int:
    try:
        lng = int(_str)
    except ValueError:
        return None
    else:
        return lng


def to_upper_or_none(_str: str) -> str:
    if _str is None or len(_str.strip()) == 0:
        return None
    else:
        return str(_str.strip().upper())


def to_date_or_none(_str: str, _format="%Y-%m-%d") -> datetime:
    try:
        date = datetime.datetime.strptime(_str, _format)
    except ValueError:
        return None
    else:
        return date


def to_float_or_none(_str: str) -> float:
    try:
        flt = float(_str)
    except ValueError:
        return None
    else:
        return flt


def to_reading_value(_str):
    if _str is None or len(_str.strip()) == 0:
        return 0
    if _str.isdigit() is False:
        return -1
    if int(_str) < 0:
        return 0
    return 1


def to_meter_size_domain(_int: int) -> int:
    if _int == 70 or _int == 7:
        return 35
    if _int == 11 or _int == 21 or _int == 22 or _int == 25 or _int == 71:
        return 30
    if _int == 66:
        return 25
    if _int == 60 or _int == 66:
        return 20
    if _int == 15 or _int == 45 or _int == 49 or _int == 53:
        return 15
    else:
        return 10
