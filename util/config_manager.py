import configparser


class ConfigManager:
    _COMMON_URL = None
    _COMMON_ID = None
    _COMMON_PW = None

    _CERT_API = None
    _CERT_PATH = None

    _IMG_API = None
    _IMG_ID = None
    _IMG_DOWNLOAD_PATH = None

    def __init__(self, ini):
        self.__get_common_conf(ini)
        self.__get_cert_conf(ini)
        self.__get_imagetransfer_conf(ini)

    def __conf_parser(self, ini):
        config = configparser.ConfigParser()
        config.read(ini)

        return config

    def __get_common_conf(self, ini):
        config = self.__conf_parser(ini)

        self._COMMON_URL = config["COMMON"]["URL"]
        self._COMMON_ID = config["COMMON"]["ID"]
        self._COMMON_PW = config["COMMON"]["PW"]

    def __get_cert_conf(self, ini):
        config = self.__conf_parser(ini)

        self._CERT_API = config["CERTIFICATION"]["API"]
        self._CERT_PATH = config["CERTIFICATION"]["CERT_PATH"]

    def __get_imagetransfer_conf(self, ini):
        config = self.__conf_parser(ini)

        self._IMG_API = config["IMAGE_TRANSFER"]["API"]
        self._IMG_ID = config["IMAGE_TRANSFER"]["DISK_ID"]
        self._IMG_DOWNLOAD_PATH = config["IMAGE_TRANSFER"]["DOWNLOAD_PATH"]

    def get_common_url(self):
        return self._COMMON_URL

    def get_common_id(self):
        return self._COMMON_ID

    def get_common_pw(self):
        return self._COMMON_PW

    def get_cert_api(self):
        return self._CERT_API

    def get_cert_path(self):
        return self._CERT_PATH

    def get_img_api(self):
        return self._IMG_API

    def get_img_download_path(self):
        return self._IMG_DOWNLOAD_PATH

    def get_img_id(self):
        return self._IMG_ID
