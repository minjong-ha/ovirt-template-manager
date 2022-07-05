import os
import requests
import shutil
import configparser
import xml.etree.ElementTree as ET

cert_params = {
    'resource': 'ca-certificate',
    'format': 'X509-PEM-CA',
}

common_headers = {
    'Version': '4',
    'Content-Type': 'application/xml',
    'Accept': 'application/xml',
}

def get_conf_parser():
    config = configparser.ConfigParser()
    config.read('config.ini')

    return config

def get_common_conf():
    config = get_conf_parser()

    common_url = config["COMMON"]["URL"]
    common_id = config["COMMON"]["ID"]
    common_pw = config["COMMON"]["PW"]

    return common_url, common_id, common_pw

def get_cert_conf():
    config = get_conf_parser()

    cert_api = config["CERTIFICATION"]["API"]
    cert_path = config["CERTIFICATION"]["CERT_PATH"]

    return cert_api, cert_path

def get_imagetransfer_conf():
    config = get_conf_parser()

    it_api = config["IMAGE_TRANSFER"]["API"]
    it_disk_id = config["IMAGE_TRANSFER"]["DISK_ID"]
    it_download_path = config["IMAGE_TRANSFER"]["DOWNLOAD_PATH"]

    return it_api, it_disk_id, it_download_path

def parse_ticket(response):
    root = ET.fromstring(response.text)
    proxy_url = root.find('proxy_url').text
    image_transfer_id = root.attrib.get('id')

    return proxy_url, image_transfer_id

def issue_cert_from_engine(common_url, cert_api, cert_path):
    url = common_url + cert_api
    
    response = requests.get(url, params = cert_params)
    os.makedirs(os.path.dirname(cert_path), exist_ok=True)
    with open(cert_path, 'w+') as f:
        f.write(bytes.decode(response.content))

def issue_ticket_for_download(it_disk_id, common_url, it_api, cert_path, common_id, common_pw):
    url = common_url + it_api
    data = '''<image_transfer> 
                <disk id="%s"/> 
                <direction>download</direction> 
            </image_transfer> 
        ''' % it_disk_id

    print(data)

    response = requests.post(url,
            headers=common_headers, data=data, verify=cert_path, 
            auth=(common_id, common_pw))

    proxy_url, image_transfer_id = parse_ticket(response)
    return proxy_url, image_transfer_id

def download_template_image(proxy_url, cert_path, it_download_path):
    with requests.get(proxy_url, stream=True, verify=cert_path) as r:
        with open(it_download_path, 'wb') as f:
            shutil.copyfileobj(r.raw, f)

def close_download(common_url, it_api, image_transfer_id, cert_path, common_id, common_pw):
    closing_url = common_url + it_api + '/' + image_transfer_id + '/finalize'
    data = "<action />"
    response = requests.post(closing_url, headers=common_headers, verify=cert_path, 
            data=data, auth=(common_id, common_pw))


if __name__ == '__main__':
    common_url, common_id, common_pw = get_common_conf()
    cert_api, cert_path = get_cert_conf()
    it_api, it_disk_id, it_download_path = get_imagetransfer_conf()

    # 1. Get certification from oVirt-engine
    issue_cert_from_engine(common_url, cert_api, cert_path)

    # 2. Request a ticket to oVirt-engine
    proxy_url, image_transfer_id = issue_ticket_for_download(it_disk_id, common_url, it_api, cert_path, common_id, common_pw)
    
    # 3. Download the template image
    download_template_image(proxy_url, cert_path, it_download_path)

    # 4. Close connection
    close_download(common_url, it_api, image_transfer_id, cert_path, common_id, common_pw)