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

    ini = "../config.ini"

    def setUp(self):
        self._conf_manager = config_manager.ConfigManager(self.ini)

        cert_path = self._conf_manager.cert_path
        path = Path(cert_path)

        if path.is_file():
            os.remove(cert_path)

    def tearDown(self):
        cert_path = self._conf_manager.cert_path
        path = Path(cert_path)

        if path.is_file():
            os.remove(cert_path)

    def test_is_config_valid(self):
        """Check config.ini validation"""

        _conf_manager = config_manager.ConfigManager(self.ini)

        self.assertIsNotNone(self._conf_manager.common_url)
        self.assertIsNotNone(self._conf_manager.common_id)
        self.assertIsNotNone(self._conf_manager.common_pw)
        print(f"common_url:         {self._conf_manager.common_url!r}")
        print(f"common_id:          {self._conf_manager.common_id!r}")
        print(f"common_pw:          {self._conf_manager.common_pw!r}\n")

        self.assertIsNotNone(self._conf_manager.cert_api)
        self.assertIsNotNone(self._conf_manager.cert_path)
        print(f"cert_api:           {self._conf_manager.cert_api!r}")
        print(f"cert_path:          {self._conf_manager.cert_path!r}\n")

        self.assertIsNotNone(self._conf_manager.img_api)
        self.assertIsNotNone(self._conf_manager.img_id)
        self.assertIsNotNone(self._conf_manager.img_download_path)
        print(f"img_api:            {self._conf_manager.img_api!r}")
        print(f"img_id:             {self._conf_manager.img_id!r}")
        print(f"img_download_path:  {self._conf_manager.img_download_path!r}\n")

        self.assertIsNotNone(self._conf_manager.template_api)
        print(f"template_api:       {self._conf_manager.template_api!r}\n")


if __name__ == "__main__":
    main()
