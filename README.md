# ovirt-template-manager
ovirt-template-manager is designed to edit, upload, download the template images on the client.
Since some versions of the oVirt-Engine do not support managing template images using web-console, ovirt-template-manager could be an alternitive or a reference.
ovirt-template-manager is implemented based on Python 3.9 and oVirt-Engine REST API for CentOS 7 + oVirt 4.3 environment.
Therefore, some of the codes or configurations should be updated for the other versions.
(Fortunately, there is a little changes in REST API as far as I know)

-----

## Working Environment
* Python 3.9
* oVirt-Engine: CentOS 7 + oVirt 4.3

## Tools
* vscode
* black, pylint (formatter)

## Configuration
'config.ini.example'represents the configurations for ovirt-template-manager.
Users have to edit some configurations to run and change the name to config.ini.
Followings mean which entries should be editted or not.

* COMMON
>* URL: oVirt-Engine FQDN   (Edit)
>* ID: oVirt-Engine ID      (Edit)
>* PW: oVirt-Engine PW      (Edit)

* CERTIFICATION
>* API                      (Fix / No Edit)
>* CERT_PATH                (Editable)

* IMAGE_TRANSFER
>* API                      (Fix / No Edit)
>* DISK_ID                  (Edit)
>* DOWNLOAD_PATH            (Edit)

* TEMPLATE
> * API						(Fix / No Edit)


## Usages
```python3 main.py ${path/to/config.ini}```
