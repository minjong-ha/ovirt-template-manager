import os
import requests
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

def parse_ticket(response):
    root = ET.fromstring(response.text)
    proxy_url = root.find('proxy_url').text
    image_transfer_id = root.attrib.get('id')

    return proxy_url, image_transfer_id

def issue_cert_from_engine():
    response = requests.get('https://engine.ovirt.tmaxos.net/ovirt-engine/services/pki-resource' ,
            params = cert_params)
    os.makedirs(os.path.dirname('/etc/cert/ovirt-engine/ca.crt'), exist_ok=True)
    with open('/etc/cert/ovirt-engine/ca.crt', 'w+') as f:
        f.write(bytes.decode(response.content))

def issue_ticket_for_download():
    data = '''<image_transfer> 
                <disk id="5b01cc68-f1b1-42a5-b96f-012bff212c28"/> 
                <direction>download</direction> 
                <inactivity_timeout>1</inactivity_timeout> 
            </image_transfer> 
        '''
    response = requests.post('https://engine.ovirt.tmaxos.net/ovirt-engine/api/imagetransfers',
            headers=common_headers, data=data, verify='/etc/cert/ovirt-engine/ca.crt', 
            auth=('admin@internal', 'tmax123!@#'))

    proxy_url, image_transfer_id = parse_ticket(response)
    return proxy_url, image_transfer_id

def download_template_image(proxy_url):
    response = requests.get(proxy_url, verify='/etc/cert/ovirt-engine/ca.crt')
    with open('/var/lib/libvirt/images//window-10-pro-system.qcow2', 'wb') as f:
        f.write(response.content)

def close_download(image_transfer_id):
    closing_url = 'https://engine.ovirt.tmaxos.net/ovirt-engine/api/imagetransfers/'+ image_transfer_id +'/finalize'
    data = "<action />"
    response = requests.post(closing_url, headers=common_headers, verify='/etc/cert/ovirt-engine/ca.crt', 
            data=data, auth=('admin@internal', 'tmax123!@#'))


if __name__ == '__main__':
    # 1. Get certification from oVirt-engine
    issue_cert_from_engine()

    # 2. Request a ticket to oVirt-engine
    proxy_url, image_transfer_id = issue_ticket_for_download()
    
    # 3. Download the template image
    download_template_image(proxy_url)

    # 4. Close connection
    close_download(image_transfer_id)
