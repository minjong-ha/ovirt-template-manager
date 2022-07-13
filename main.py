"""
Created by "Minjong Ha" on 2022/07/05
"""

import sys

from utils.config_manager import ConfigManager
from utils.download_manager import DownloadManager
from utils.info_manager import InfoManager

if __name__ == "__main__":
    try:
        ini = sys.argv[1]
    except:
        print("Missing config.ini argument")
        print("Usage: python3 main.py ${path/to/config.ini}")
        sys.exit()

    conf_manager = ConfigManager(ini)
    dl_manager = DownloadManager(conf_manager)
    info_manager = InfoManager(conf_manager)

    info_manager.list_all_templates()
    #dl_manager.download_image()
