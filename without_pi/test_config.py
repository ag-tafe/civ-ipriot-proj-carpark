import unittest
import os

import tomli

from without_pi.main02 import parse_config as pc

class TestConfigParsing(unittest.TestCase):
    def test_toml_config_file_exists(self):
        '''Make sure a file with toml extension exists in the current directory.'''
        smartpark_path = os.getcwd()
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
        '''Configuration file parsing works successfully.'''
        file_name = 'test_tomli.toml'
        config_string = '''
        [parking_lot]
        location = "Moondalup City Square Parking"
        total_spaces = 192
        broker_host = "localhost"
        broker_port = 1883
        '''
        # https://realpython.com/working-with-files-in-python/#pythons-with-open-as-pattern
        with open(file_name, 'w') as handle:
            handle.write(config_string)

        # getting a dictionary with values from string
        config = tomli.loads(config_string)

        parking_lot = pc('test_tomli.toml')
        parking_lot = parking_lot['parking_lot']
        self.assertEqual(parking_lot['location'], "Moondalup City Square Parking")
        self.assertEqual(parking_lot['total_spaces'], 192)
        self.assertEqual(parking_lot['broker_host'], "localhost")
        self.assertEqual(parking_lot['broker_port'], 1883)

if __name__ == '__main__':
    unittest.main()