"""
Created by "Minjong Ha" on 2022/07/29
"""

from unittest import TestCase, main
from pathlib import Path

import sys
import os
from os import path

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from utils import config_manager
from utils import download_manager
from utils import info_manager


class UtilTestCase(TestCase):
    """
    UtilTestCase presents the test cases for modules in utils directory
    : config_manager, download_manager, and info_manager
    """

    def test_is_config_valid(self):
        """Check config.ini validation"""

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
        """Check the host is connected to ovirt-engine"""

        ini = "../config.ini"
        _conf_manager = config_manager.ConfigManager(ini)

        cert_path = _conf_manager.cert_path
        path = Path(cert_path)

        if path.is_file():
            os.remove(cert_path)

        _download_manager = download_manager.DownloadManager(_conf_manager)
        _download_manager.issue_cert_from_engine()

        assert path.is_file()

        print(f"ovirt-engine({_conf_manager.common_url} is connected: {path.is_file()})")


if __name__ == "__main__":
    main()
