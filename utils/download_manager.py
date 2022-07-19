"""
Created by "Minjong Ha" on 2022/07/05
"""

import os
import shutil
import xml.etree.ElementTree as ET
import requests

from .config_manager import cert_params
from .config_manager import common_headers


class DownloadManager:
    """
    DownloadManager has responsibility to manage the temaplate images.
    It can download, edit, list the template images in the oVirt cluster.
    With the help of ConfigManager, it is easy to configure the parameters for management.
    """

    _conf_manager = None

    def __init__(self, config_manager):
        self._conf_manager = config_manager

    def __parse_ticket(self, response):
        root = ET.fromstring(response.text)
        proxy_url = root.find("proxy_url").text
        image_transfer_id = root.attrib.get("id")

        return proxy_url, image_transfer_id

    def __issue_cert_from_engine(self):
        url = self._conf_manager.get_cert_req_url()
        cert_path = self._conf_manager.get_cert_path()

        response = requests.get(url, params=cert_params)
        os.makedirs(os.path.dirname(cert_path), exist_ok=True)
        with open(cert_path, "w+") as file:
            file.write(bytes.decode(response.content))

    def __issue_ticket_for_download(self, id):
        url = self._conf_manager.get_download_req_url()
        cert_path = self._conf_manager.get_cert_path()
        common_id = self._conf_manager.get_common_id()
        common_pw = self._conf_manager.get_common_pw()

        if id is None:
            disk_id = self._conf_manager.get_img_id()
        else:
            disk_id = id

        data = f"""
                <image_transfer>
                    <disk id="{disk_id}"/>
                    <direction>download</direction>
                </image_transfer>
            """

        response = requests.post(
            url,
            headers=common_headers,
            data=data,
            verify=cert_path,
            auth=(common_id, common_pw),
        )

        proxy_url, image_transfer_id = self.__parse_ticket(response)
        return proxy_url, image_transfer_id

    def __download_template_image(self, proxy_url):
        cert_path = self._conf_manager.get_cert_path()
        img_download_path = self._conf_manager.get_img_download_path()

        with requests.get(proxy_url, stream=True, verify=cert_path) as r:
            with open(img_download_path, "wb") as f:
                shutil.copyfileobj(r.raw, f)

    def __close_download(self, image_transfer_id):
        cert_path = self._conf_manager.get_cert_path()
        common_id = self._conf_manager.get_common_id()
        common_pw = self._conf_manager.get_common_pw()
        closing_url = self._conf_manager.get_closing_url(image_transfer_id)

        data = "<action />"
        response = requests.post(
            closing_url,
            headers=common_headers,
            verify=cert_path,
            data=data,
            auth=(common_id, common_pw),
        )

    def download_image_with_id(self, disk_id):
        """
        Download the template image from oVirt-engine using REST API
        """
        # 1. Get certification from oVirt-engine
        self.__issue_cert_from_engine()

        # 2. Request a ticket to oVirt-engine
        proxy_url, image_transfer_id = self.__issue_ticket_for_download(disk_id)

        # 3. Download the template image
        self.__download_template_image(proxy_url)

        # 4. Close connection
        self.__close_download(image_transfer_id)
