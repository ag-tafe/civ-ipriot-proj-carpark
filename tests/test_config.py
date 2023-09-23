import unittest
import os

import tomli  # you can use toml, json,yaml, or ryo for your config file

#import smartpark.parse_config as pc
from config_parser import parse_config as pc

class TestConfigParsing(unittest.TestCase):
    def test_toml_config_file_exists(self):
        '''Make sure a file with toml extension exists in "smartpark" directory.'''
        base_path = os.getcwd()
        # https://www.geeksforgeeks.org/get-parent-of-current-directory-using-python/
        parent_path = os.path.abspath(os.path.join(base_path, os.pardir))
        smartpark_path = os.path.join(parent_path, 'smartpark')
        files = []
        # getting a list of files
        # https://realpython.com/working-with-files-in-python/
        for entry in os.listdir(smartpark_path):
            if os.path.isfile(os.path.join(smartpark_path, entry)):
                files.append(entry)
        # get extensions of files
        extensions = []
        for file in files:
            extensions.append(file.split('.')[1])
        self.assertIn('toml', extensions)


    def test_parse_config_has_correct_location_and_spaces(self):
        file_name = 'test_tomli.toml'
        config_string = '''
        [parking_lot]
        location = "Moondalup City Square Parking"
        total_spaces = 192
        broker_host = "localhost"
        broker_port = 1883
        '''
        # writing into the test file
        handle = open(file_name, "w")
        handle.write(config_string)
        handle.close()

        # getting a dictionary with values from string
        config = tomli.loads(config_string)

        #parking_lot = pc.parse_config(config)
        parking_lot = pc('test_tomli.toml')
        parking_lot = parking_lot['parking_lot']
        self.assertEqual(parking_lot['location'], config["parking_lot"]["location"])
        self.assertEqual(parking_lot['total_spaces'], config["parking_lot"]["total_spaces"])
        self.assertEqual(parking_lot['broker_host'], config["parking_lot"]['broker_host'])
        self.assertEqual(parking_lot['broker_port'], config["parking_lot"]['broker_port'])

