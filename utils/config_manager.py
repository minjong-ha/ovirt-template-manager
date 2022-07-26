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

    def __init__(self, ini):
        self._config = configparser.ConfigParser()

        self.__get_common_conf(ini)
        self.__get_cert_conf(ini)
        self.__get_imagetransfer_conf(ini)
        self.__get_template_conf(ini)

    def __conf_parser(self, ini):
        self._config.read(ini)

        config = configparser.ConfigParser()
        config.read(ini)

        return config

    def __get_common_conf(self, ini):
        config = self.__conf_parser(ini)

        self.common_url = config["COMMON"]["URL"]
        self.common_id = config["COMMON"]["ID"]
        self.common_pw = config["COMMON"]["PW"]

    def __get_cert_conf(self, ini):
        config = self.__conf_parser(ini)

        self.cert_api = config["CERTIFICATION"]["API"]
        self.cert_path = config["CERTIFICATION"]["CERT_PATH"]

    def __get_imagetransfer_conf(self, ini):
        config = self.__conf_parser(ini)

        self.img_api = config["IMAGE_TRANSFER"]["API"]
        self.img_id = config["IMAGE_TRANSFER"]["DISK_ID"]
        self.img_download_path = config["IMAGE_TRANSFER"]["DOWNLOAD_PATH"]

    def __get_template_conf(self, ini):
        config = self.__conf_parser(ini)

        self.template_api = config["TEMPLATE"]["API"]

    @property
    def cert_req_url(self):
        """return cert_req_url for download certification"""
        return self.common_url + self.cert_api

    @property
    def download_req_url(self):
        """return download_req_url for issue the ticket"""
        return self.common_url + self.img_api

    @property
    def template_url(self):
        """return template_url to get info of all templates"""
        return self.common_url + self.template_api

    @property
    def closing_url(self):
        """
        return closing_url for download finalize
        id: image trasfer id that issued by ovirt-engine
        """
        return self._closing_url

    @closing_url.setter
    def closing_url(self, image_transfer_id):
        self._closing_url = self.common_url + self.img_api + "/" + image_transfer_id + "/finalize"

    @property
    def template_diskattachments_url(self):
        """return disk_attachments url for disk_id it takes"""
        return self._template_diskattachments_url

    @template_diskattachments_url.setter
    def template_diskattachments_url(self, disk_id):
        self._template_diskattachments_url = (
            self.template_url + "/" + disk_id + "/diskattachments"
        )
