"""
Created by "Minjong Ha" on 2022/07/05
"""
import sys
import os

from os import path
from pathlib import Path

sys.path.append(path.dirname(path.dirname(path.dirname(path.abspath(__file__)))))

from utils.config_manager import cert_params
from utils.config_manager import common_headers

import os
import math
import xml.etree.ElementTree as ET
import requests


def human_readable_filesize(byte_size: str) -> str:
    byte_size = int(byte_size)
    if byte_size == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(byte_size, 1024)))
    p = math.pow(1024, i)
    s = round(byte_size / p, 2)

    return f"{s} {size_name[i]}"


class DownloadManager:
    """
    DownloadManager has responsibility to manage the temaplate images.
    It can download, edit, list the template images in the oVirt cluster.
    With the help of ConfigManager, it is easy to configure the parameters for management.
    """

    def __init__(self, config_manager):
        self._conf_manager = config_manager

        # get certification from ovirt-engine
        self.__certificate_engine()

    def __certificate_engine(self):
        url = (
            self._conf_manager.cert_init_url
            + self._conf_manager.cert_api
            + "?resource=ca-certificate&format=X509-PEM-CA"
        )

        cert_path = path.dirname(self._conf_manager.cert_path)
        if not os.path.exists(cert_path):
            os.makedirs(cert_path)

        response = requests.get(url, params=cert_params)
        with open(self._conf_manager.cert_path, "wb") as f:
            f.write(response.content)

    def __parse_ticket(self, response):
        root = ET.fromstring(response.text)
        proxy_url = root.find("proxy_url").text
        image_transfer_id = root.attrib.get("id")

        return proxy_url, image_transfer_id

    def __issue_ticket_for_download(self, id):
        url = self._conf_manager.download_req_url
        cert_path = self._conf_manager.cert_path
        common_id = self._conf_manager.common_id
        common_pw = self._conf_manager.common_pw

        if id is None:
            disk_id = self._conf_manager.img_id
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
        cert_path = self._conf_manager.cert_path
        img_download_path = self._conf_manager.img_download_path

        with open(img_download_path, "wb") as f:
            response = requests.get(proxy_url, stream=True, verify=cert_path)
            total_length = response.headers.get("content-length")
            print(
                f"Downloading {total_length} bytes ({human_readable_filesize(total_length)})"
            )

            if total_length is None:
                f.write(response.content)
            else:
                dl = 0
                total_length = int(total_length)
                for data in response.iter_content(chunk_size=4096):
                    dl += len(data)
                    f.write(data)
                    done = int(100 * dl / total_length)
                    sys.stdout.write(
                        f"\r[{'#' * done}{' ' * (100 - done)}].....{(dl / total_length * 100):.2f} %"
                    )
                    sys.stdout.flush()
            print()

    def __close_download(self, image_transfer_id):
        cert_path = self._conf_manager.cert_path
        common_id = self._conf_manager.common_id
        common_pw = self._conf_manager.common_pw
        self._conf_manager.closing_url = image_transfer_id
        closing_url = self._conf_manager.closing_url

        data = "<action />"
        response = requests.post(
            closing_url,
            headers=common_headers,
            verify=cert_path,
            data=data,
            auth=(common_id, common_pw),
        )

    def __remove_old_cert(self):
        cert_path = self._conf_manager.cert_path
        file_path = Path(cert_path)
        if file_path.is_file():
            os.remove(cert_path)

    def issue_cert_from_engine(self):
        self.__certificate_engine()

    def download_image_with_id(self, disk_id):
        """
        Download the template image from oVirt-engine using REST API
        """

        # 1. Request a ticket to oVirt-engine
        proxy_url, image_transfer_id = self.__issue_ticket_for_download(disk_id)

        # 2. Download the template image
        self.__download_template_image(proxy_url)

        # 3. Close connection
        self.__close_download(image_transfer_id)
