"""
Created by "Minjong Ha" on 2022/07/05
"""

import configparser

cert_params = {
    "resource": "ca-certificate",
    "format": "X509-PEM-CA",
}

common_headers = {
    "Version": "4",
    "Content-Type": "application/xml",
    "Accept": "application/xml",
}


class ConfigManager:
    """
    ConfigManager has a responsibility to load the configurations from config.ini.
    Configurations will be used by other managers.
    """

    _common_url = None
    _common_id = None
    _common_pw = None

    _cert_api = None
    _cert_path = None

    _img_api = None
    _img_id = None
    _img_download_path = None

    _config = None

    def __init__(self, ini):
        self.__get_common_conf(ini)
        self.__get_cert_conf(ini)
        self.__get_imagetransfer_conf(ini)

    def __conf_parser(self, ini):
        self._config = configparser.ConfigParser()
        self._config.read(ini)

        config = configparser.ConfigParser()
        config.read(ini)

        return config

    def __get_common_conf(self, ini):
        config = self.__conf_parser(ini)

        self._common_url = config["COMMON"]["URL"]
        self._common_id = config["COMMON"]["ID"]
        self._common_pw = config["COMMON"]["PW"]

    def __get_cert_conf(self, ini):
        config = self.__conf_parser(ini)

        self._cert_api = config["CERTIFICATION"]["API"]
        self._cert_path = config["CERTIFICATION"]["CERT_PATH"]

    def __get_imagetransfer_conf(self, ini):
        config = self.__conf_parser(ini)

        self._img_api = config["IMAGE_TRANSFER"]["API"]
        self._img_id = config["IMAGE_TRANSFER"]["DISK_ID"]
        self._img_download_path = config["IMAGE_TRANSFER"]["DOWNLOAD_PATH"]

    def get_common_url(self):
        """return common_url"""
        return self._common_url

    def get_common_id(self):
        """return common_id"""
        return self._common_id

    def get_common_pw(self):
        """return common_pw"""
        return self._common_pw

    def get_cert_api(self):
        """return cert_api"""
        return self._cert_api

    def get_cert_path(self):
        """return cert_path"""
        return self._cert_path

    def get_img_api(self):
        """return img_api"""
        return self._img_api

    def get_img_download_path(self):
        """return img_download_path"""
        return self._img_download_path

    def get_img_id(self):
        """return img_id"""
        return self._img_id
