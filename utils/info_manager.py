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
    _template_list = None

    def __init__(self, config_manager):
        self._conf_manager = config_manager
        self.__get_templates()

    def __get_templates(self):
        url = self._conf_manager.get_template_url()
        cert_path = self._conf_manager.get_cert_path()
        common_id = self._conf_manager.get_common_id()
        common_pw = self._conf_manager.get_common_pw()

        response = requests.get(
            url, headers=common_headers, verify=cert_path, auth=(common_id, common_pw)
        )

        root = ET.fromstring(response.text)
        self._template_list = list(root.iter("template"))

    def __get_diskattachment(self, id):
        url = self._conf_manager.get_template_url() + "/" + id + "/diskattachments"
        cert_path = self._conf_manager.get_cert_path()
        common_id = self._conf_manager.get_common_id()
        common_pw = self._conf_manager.get_common_pw()

        response = requests.get(
            url, headers=common_headers, verify=cert_path, auth=(common_id, common_pw)
        )
        root = ET.fromstring(response.text)

        disk_list = list(root.iter("disk_attachment"))
        print(f"Number of attachment: {len(disk_list)}")
        for disk in disk_list:
            return disk.attrib.get("id")

    def __list_template_info(self, template):
            template_name = template.find("name").text
            template_desc = template.find("description").text
            template_comment = template.find("comment").text
            template_ver_name = template.find("version").find("version_name").text
            template_ver_number = template.find("version").find("version_number").text
            template_disk_id = self.__get_diskattachment(template.attrib.get("id"))

            print(f"Name: \t\t{template_name}")
            print(f"Description: \t{template_desc}")
            print(f"Comment: \t{template_comment}")
            print(f"Version: \t{template_ver_name} - {template_ver_number}")
            print(f"disk_id: \t{template_disk_id}")
            print("=============================================================")
            
    def list_all_templates(self):
        print("LIST ALL TEMPLATES")
        print(f"Number of Templates: {len(self._template_list)}")

        for idx, template in enumerate(self._template_list):
            print(f"Template Index: {idx}")
            self.__list_template_info(template)

    def list_template_info(self, idx):
        template = self._template_list[idx]

        self.__list_template_info(template)

    def get_disk_id(self, idx):
        template = self._template_list[idx]

        return self.__get_diskattachment(template.attrib.get("id"))
