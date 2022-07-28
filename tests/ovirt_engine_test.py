import sys
from os import path
sys.path.append(path.dirname( path.dirname( path.abspath(__file__) ) ))

from utils import config_manager
from utils import download_manager
from utils import info_manager

from unittest import TestCase, main

class UtilTestCase(TestCase):
    def test_config_manager(self):
        self.assertEqual('hello', 'hello')

    def test_connect_to_ovirt_engine(self):
        self.assertEqual('hello', 'hello')


if __name__ == '__main__':
    main()