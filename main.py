"""
main.py is the main file to run ovirt-tmeplate-manager
"""

from utils.config_manager import ConfigManager
from utils.download_manager import DownloadManager

conf_manager = ConfigManager("config.ini")
dl_manager = DownloadManager(conf_manager)

if __name__ == "__main__":
    dl_manager.download_image()
