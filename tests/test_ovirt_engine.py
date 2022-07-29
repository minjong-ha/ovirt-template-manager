import sys
import os
from os import path
sys.path.append(path.dirname( path.dirname( path.abspath(__file__) ) ))

from utils import config_manager
from utils import download_manager
from utils import info_manager

from unittest import TestCase, main
from pathlib import Path

class UtilTestCase(TestCase):
    
    def test_is_config_valid(self):
        ini = "../config.ini"
        _conf_manager = config_manager.ConfigManager(ini)

        self.assertIsNotNone(_conf_manager.common_url)
        print(f"common_url:         {_conf_manager.common_url!r}")
        self.assertIsNotNone(_conf_manager.common_id)
        print(f"common_id:          {_conf_manager.common_id!r}")
        self.assertIsNotNone(_conf_manager.common_pw)
        print(f"common_pw:          {_conf_manager.common_pw!r}\n")

        self.assertIsNotNone(_conf_manager.cert_api)
        print(f"cert_api:           {_conf_manager.cert_api!r}")
        self.assertIsNotNone(_conf_manager.cert_path)
        print(f"cert_path:          {_conf_manager.cert_path!r}\n")

        self.assertIsNotNone(_conf_manager.img_api)
        print(f"img_api:            {_conf_manager.img_api!r}")
        self.assertIsNotNone(_conf_manager.img_id)
        print(f"img_id:             {_conf_manager.img_id!r}")
        self.assertIsNotNone(_conf_manager.img_download_path)
        print(f"img_download_path:  {_conf_manager.img_download_path!r}\n")

        self.assertIsNotNone(_conf_manager.template_api)
        print(f"template_api:       {_conf_manager.template_api!r}\n")

    def test_is_connected(self):
        ini = "../config.ini"
        _conf_manager = config_manager.ConfigManager(ini)

        cert_path = _conf_manager.cert_path
        path = Path(cert_path)

        if path.is_file():
            os.remove(cert_path)

        _download_manager = download_manager.DownloadManager(_conf_manager)
        _download_manager.issue_cert_from_engine()

        assert path.is_file()


if __name__ == '__main__':
    main()