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

if __name__ == '__main__':
    # Using requests(curl) and download template through the python
    # 1. Get certification from oVirt-engine
    #    Download the certification in the /etc/kpi/ovirt-engine
    response = requests.get('https://engine.ovirt.tmaxos.net/ovirt-engine/services/pki-resource', 
            params=cert_params)
    os.makedirs(os.path.dirname('/etc/cert/ovirt-engine/ca.crt'), exist_ok=True)
    with open('/etc/cert/ovirt-engine/ca.crt', 'w+') as f:
        f.write(bytes.decode(response.content))

    # 2. Request a ticket to oVirt-engine
    #    Get proxy URL (download URL) and print it
    data = '''<image_transfer> 
                <disk id="358f6326-999a-45d0-9e84-bebfdeb543d0"/> 
                <direction>download</direction> 
                <inactivity_timeout>1</inactivity_timeout> 
            </image_transfer> 
        '''

    response = requests.post('https://engine.ovirt.tmaxos.net/ovirt-engine/api/imagetransfers',
            headers=common_headers, data=data, verify='/etc/cert/ovirt-engine/ca.crt', 
            auth=('admin@internal', 'tmax123!@#'))

    # Require parsing xml. Select proxy url and image_transfer id
    root = ET.fromstring(response.text)
    proxy_url = root.find('proxy_url').text
    image_transfer_id = root.attrib.get('id')
    print(proxy_url)
    print(image_transfer_id)
    
    # 3. Download the template image
    response = requests.get(proxy_url, verify='/etc/cert/ovirt-engine/ca.crt')
    with open('/home/minjong_ha/tmp', 'wb') as f:
        f.write(response.content)

    # 4. Close connection
    closing_url = 'https://engine.ovirt.tmaxos.net/ovirt-engine/api/imagetransfers/'+ image_transfer_id +'/finalize'
    data = "<action />"
    response = requests.post(closing_url, headers=common_headers, verify='/etc/cert/ovirt-engine/ca.crt', 
            data=data, auth=('admin@internal', 'tmax123!@#'))
