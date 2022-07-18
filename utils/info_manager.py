"""
Created by "Minjong Ha" on 2022/07/06
"""

import requests
import xml.etree.ElementTree as ET

from .config_manager import cert_params
from .config_manager import common_headers


class InfoManager:
    """
    InfoManager has responsibility to list the images in the disks.
    It can reformats the xml info of the images into the human-readable format.
    """

    _conf_manager = None

    def __init__(self, config_manager):
        self._conf_manager = config_manager

    def __get_diskattachment(self, id):
        print(id)
        url = self._conf_manager.get_template_url() + "/" + id + "/diskattachments"
        cert_path = self._conf_manager.get_cert_path()
        common_id = self._conf_manager.get_common_id()
        common_pw = self._conf_manager.get_common_pw()

        response = requests.get(
            url, headers=common_headers, verify=cert_path, auth=(common_id, common_pw)
        )
        root = ET.fromstring(response.text)

        for disk_attachment in root.iter("disk_attachment"):
            print(disk_attachment.attrib.get("id"))

    def list_all_templates(self):
        print("LIST ALL TEMPLATES")
        url = self._conf_manager.get_template_url()
        cert_path = self._conf_manager.get_cert_path()
        common_id = self._conf_manager.get_common_id()
        common_pw = self._conf_manager.get_common_pw()

        response = requests.get(
            url, headers=common_headers, verify=cert_path, auth=(common_id, common_pw)
        )

        root = ET.fromstring(response.text)
        for template in root.iter("template"):
            print(template.find("name").text)
            print(template.find("description").text)
            print(template.find("comment").text)
            print(template.find("version").find("version_name").text)
            print(template.find("version").find("version_number").text)
            self.__get_diskattachment(template.attrib.get("id"))
            print("=============================================================")
