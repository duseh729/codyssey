import random
import logging
import os

# 로그 설정 (파일로 저장)
logging.basicConfig(
    level=logging.DEBUG,  # 모든 레벨 로그 저장
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    filename=os.path.join(os.path.dirname(__file__), 'app.log'),  # 로그 파일 지정
    filemode="a"  # "w"이면 기존 파일 덮어쓰기, "a"이면 추가
)

def logging_value(value):
    for key in value:
        logging.info(f'{key}: {value[key]}')

def round_num(num):
    return round(num, 2)

class DummySensor:
    def __init__(self):
        self.__env_values = {
            'mars_base_internal_temperature': None,
            'mars_base_external_temperature': None,
            'mars_base_internal_humidity': None,
            'mars_base_external_illuminance': None,
            'mars_base_internal_co2': None,
            'mars_base_internal_oxygen': None
        }

    def set_env(self):
        self.__env_values['mars_base_internal_temperature'] = round_num(random.uniform(18, 31))
        self.__env_values['mars_base_external_temperature'] = round_num(random.uniform(0, 22))
        self.__env_values['mars_base_internal_humidity'] = round_num(random.uniform(50, 61))
        self.__env_values['mars_base_external_illuminance'] = round_num(random.uniform(500, 715))
        self.__env_values['mars_base_internal_co2'] = round_num(random.uniform(0.02, 0.1))
        self.__env_values['mars_base_internal_oxygen'] = round_num(random.uniform(4, 7))
    
    def get_env(self):
        logging_value(self.__env_values)
        return self.__env_values
    
if __name__ == "__main__":
    ds = DummySensor()
    ds.set_env()

    ds_value = ds.get_env()
    unit = {
        'mars_base_internal_temperature': '℃',
        'mars_base_external_temperature': '℃',
        'mars_base_internal_humidity': '%',
        'mars_base_external_illuminance': 'W/m²',
        'mars_base_internal_co2': '%',
        'mars_base_internal_oxygen': '%'
    }

    for key in ds_value:
        print(f'{key}: {ds_value[key]}{unit[key]}')