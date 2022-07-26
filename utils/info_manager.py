"""
Created by "Minjong Ha" on 2022/07/06
"""

from .config_manager import common_headers

import xml.etree.ElementTree as ET
import requests

class InfoManager:
    """
    InfoManager has responsibility to list the images in the disks.
    It can reformats the xml info of the images into the human-readable format.
    """

    def __init__(self, config_manager):
        self._conf_manager = config_manager
        self.__get_templates()

    def __sort_templates_by_version_number(self, parent):
        parent[:] = sorted(parent, key=lambda child: (child.find("version").find("version_number").text))

    def __get_templates(self):
        url = self._conf_manager.template_url
        cert_path = self._conf_manager.cert_path
        common_id = self._conf_manager.common_id
        common_pw = self._conf_manager.common_pw

        response = requests.get(
            url, headers=common_headers, verify=cert_path, auth=(common_id, common_pw)
        )

        root = ET.fromstring(response.text)

        #========================================================================
        template_name_list = []
        unique_template_name_list = []
        sorted_template_list = []

        # 1. extract name list
        for template in root:
            template_name_list.append(template.find("name").text)
        unique_template_names = set(template_name_list)
        for template in unique_template_names:
            unique_template_name_list.append(template)
        print(unique_template_name_list)

        unique_template_name_list.sort()
            
        # 2. choose each templates having same name
        for template_name in unique_template_name_list:
            print(template_name)
            template_list_by_name = []
            for template in root.findall("template"):
                if template.find("name").text == template_name:
                    template_list_by_name.append(template)
            # 3. sort each groups with version.version_number
            self.__sort_templates_by_version_number(template_list_by_name)
            # 4. concantenate them
            sorted_template_list = sorted_template_list + template_list_by_name

        self._template_list = sorted_template_list
        #========================================================================
        #self._template_list = list(root.iter("template"))

    def __get_diskattachment(self, disk_id):
        self._conf_manager.template_diskattachments_url = disk_id
        url = self._conf_manager.template_diskattachments_url
        cert_path = self._conf_manager.cert_path
        common_id = self._conf_manager.common_id
        common_pw = self._conf_manager.common_pw

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
        """print the info of all templates"""

        print("LIST ALL TEMPLATES")
        print(f"Number of Templates: {len(self._template_list)}")

        for idx, template in enumerate(self._template_list):
            print(f"Template Index: {idx}")
            self.__list_template_info(template)

    def list_template_info(self, idx):
        """print the info of selected template"""
        template = self._template_list[idx]

        self.__list_template_info(template)

    def get_disk_id(self, idx):
        """return the disk_id of template (disk_attachment)"""
        template = self._template_list[idx]

        return self.__get_diskattachment(template.attrib.get("id"))
