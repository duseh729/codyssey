import sys
import os
import json
import time

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from problem6 import mars_mission_computer as mc6

class MissionComputer:
    # 아래 처럼 하면 클래스 변수라서 모든 인스턴스가 값을 공유하게 됨.
    # __env_values = {
    #     'mars_base_internal_temperature': None,
    #     'mars_base_external_temperature': None,
    #     'mars_base_internal_humidity': None,
    #     'mars_base_external_illuminance': None,
    #     'mars_base_internal_co2': None,
    #     'mars_base_internal_oxygen': None
    # }
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

if __name__ == '__main__':
    RunComputer = MissionComputer();
    RunComputer.get_sensor_data()
