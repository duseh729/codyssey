import sys
import os
import json
import time
import platform
import psutil

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from problem6 import mars_mission_computer as mc6

class MissionComputer:
    def __init__(self):
        self.__env_values = {
            'mars_base_internal_temperature': None,
            'mars_base_external_temperature': None,
            'mars_base_internal_humidity': None,
            'mars_base_external_illuminance': None,
            'mars_base_internal_co2': None,
            'mars_base_internal_oxygen': None
        }

    def get_sensor_data(self):
        ds = mc6.DummySensor()
        while True:
            ds.set_env()
            ds_get_value = ds.get_env();

            self.__env_values['mars_base_internal_temperature'] = ds_get_value['mars_base_internal_temperature']
            self.__env_values['mars_base_external_temperature'] = ds_get_value['mars_base_external_temperature']
            self.__env_values['mars_base_internal_humidity'] = ds_get_value['mars_base_internal_humidity']
            self.__env_values['mars_base_external_illuminance'] = ds_get_value['mars_base_external_illuminance']
            self.__env_values['mars_base_internal_co2'] = ds_get_value['mars_base_internal_co2']
            self.__env_values['mars_base_internal_oxygen'] = ds_get_value['mars_base_internal_oxygen']

            print(self.to_json())

            time.sleep(5)

    def to_json(self):
        return json.dumps(self.__env_values, indent=4)
    

    def get_mission_computer_info(self):
        try:
            info = {
                'operating_system': platform.system(),
                'os_version': platform.version(),
                'cpu_type': platform.processor(),
                'cpu_cores': psutil.cpu_count(logical=False),
                'memory_size_gb': round(psutil.virtual_memory().total / (1024 ** 3), 2)
            }
            print(self.to_json(info))
            return info
        except Exception as e:
            print(f'get_mission_computer_info error: {e}')
            return {}

    def get_mission_computer_load(self):
        try:
            load_info = {
                'cpu_usage_percent': psutil.cpu_percent(interval=1),
                'memory_usage_percent': psutil.virtual_memory().percent
            }
            print(self.to_json(load_info))
            return load_info
        except Exception as e:
            print(f'get_mission_computer_load error: {e}')
            return {}

if __name__ == '__main__':
    runComputer = MissionComputer()
    runComputer.get_mission_computer_info()
    runComputer.get_mission_computer_load()