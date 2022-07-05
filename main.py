import os
import requests
import shutil
import xml.etree.ElementTree as ET

from util.config_manager import ConfigManager
from util.config_manager import cert_params
from util.config_manager import common_headers

conf_manager = ConfigManager("config.ini")


def parse_ticket(response):
    root = ET.fromstring(response.text)
    proxy_url = root.find("proxy_url").text
    image_transfer_id = root.attrib.get("id")

    return proxy_url, image_transfer_id


def issue_cert_from_engine():
    url = conf_manager.get_common_url() + conf_manager.get_cert_api()
    cert_path = conf_manager.get_cert_path()

    response = requests.get(url, params=cert_params)
    os.makedirs(os.path.dirname(cert_path), exist_ok=True)
    with open(cert_path, "w+") as f:
        f.write(bytes.decode(response.content))


def issue_ticket_for_download():
    url = conf_manager.get_common_url() + conf_manager.get_img_api()
    disk_id = conf_manager.get_img_id()
    cert_path = conf_manager.get_cert_path()
    common_id = conf_manager.get_common_id()
    common_pw = conf_manager.get_common_pw()

    data = (
        """<image_transfer>
                <disk id="%s"/>
                <direction>download</direction>
            </image_transfer>
        """
        % disk_id
    )

    response = requests.post(
        url,
        headers=common_headers,
        data=data,
        verify=cert_path,
        auth=(common_id, common_pw),
    )

    proxy_url, image_transfer_id = parse_ticket(response)
    return proxy_url, image_transfer_id


def download_template_image(proxy_url):
    cert_path = conf_manager.get_cert_path()
    img_download_path = conf_manager.get_img_download_path()

    with requests.get(proxy_url, stream=True, verify=cert_path) as r:
        with open(img_download_path, "wb") as f:
            shutil.copyfileobj(r.raw, f)


def close_download(image_transfer_id):
    cert_path = conf_manager.get_cert_path()
    common_id = conf_manager.get_common_id()
    common_pw = conf_manager.get_common_pw()
    common_url = conf_manager.get_common_url()
    img_api = conf_manager.get_img_api()
    closing_url = common_url + img_api + "/" + image_transfer_id + "/finalize"

    data = "<action />"
    response = requests.post(
        closing_url,
        headers=common_headers,
        verify=cert_path,
        data=data,
        auth=(common_id, common_pw),
    )


if __name__ == "__main__":
    # 1. Get certification from oVirt-engine
    issue_cert_from_engine()

    # 2. Request a ticket to oVirt-engine
    proxy_url, image_transfer_id = issue_ticket_for_download()

    # 3. Download the template image
    download_template_image(proxy_url)

    # 4. Close connection
    close_download(image_transfer_id)
