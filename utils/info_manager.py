"""
Created by "Minjong Ha" on 2022/07/06
"""

class InfoManager:
    """
    InfoManager has responsibility to list the images in the disks.
    It can reformats the xml info of the images into the human-readable format.
    """

    _conf_manager = None
    
    def __init__(self, config_manager):
        self._conf_manager = config_manager
    
    # TODO(220706, Minjong Ha: implement list images or templates?)

