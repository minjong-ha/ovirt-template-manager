"""
Created by "Minjong Ha" on 2022/07/05
"""

import sys
import os

from pathlib import Path
from os import path

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from utils.config_manager import ConfigManager
from utils.download_manager import DownloadManager
from utils.info_manager import InfoManager
from utils.notify_manager import NotifyManager


def print_empty_line():
    print()


if __name__ == "__main__":

    try:
        ini = sys.argv[1]
    except:
        print("Missing config.ini argument")
        print("Usage: python3 main.py ${path/to/config.ini}")
        sys.exit()

    conf_manager = ConfigManager(ini)
    https_cert_path = path.dirname(conf_manager.cert_path)
    if not os.path.exists(https_cert_path):
        os.makedirs(https_cert_path)

    dl_manager = DownloadManager(conf_manager)
    info_manager = InfoManager(conf_manager)

    info_manager.list_all_templates()
    print_empty_line()
    print_empty_line()

    index = input("Select the template you want to download: ")
    print_empty_line()

    # Double check the selected template
    info_manager.list_template_info(int(index))
    check = input("Is this template you want? {y/n): ")
    disk_id = info_manager.get_disk_id(int(index))

    if check in ("y", "yes", "Y", "YES", "Yes"):
        dl_manager.download_image_with_id(disk_id)
    else:
        print("Download canceled")
        sys.exit()
