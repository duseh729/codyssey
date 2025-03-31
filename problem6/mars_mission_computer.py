import random

def rount_num(num):
    return round(num, 2)

class DummySensor:
    def __init__(self):
        self.env_values = {
            'mars_base_internal_temperature': None,
            'mars_base_external_temperature': None,
            'mars_base_internal_humidity': None,
            'mars_base_external_illuminance': None,
            'mars_base_internal_co2': None,
            'mars_base_internal_oxygen': None
        }

    def set_env(self):
        self.env_values['mars_base_internal_temperature'] = rount_num(random.uniform(18, 31))
        self.env_values['mars_base_external_temperature'] = rount_num(random.uniform(0, 22))
        self.env_values['mars_base_internal_humidity'] = rount_num(random.uniform(50, 61))
        self.env_values['mars_base_external_illuminance'] = rount_num(random.uniform(500, 715))
        self.env_values['mars_base_internal_co2'] = rount_num(random.uniform(0.02, 0.1))
        self.env_values['mars_base_internal_oxygen'] = rount_num(random.uniform(4, 7))
    
    def get_env(self):
        return self.env_values
    
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