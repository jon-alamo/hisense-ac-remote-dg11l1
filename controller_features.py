import code_generation as cg
import json

with open('base_codes.json', 'r') as f:
    _codes = json.load(f)


_MODES = {
    'heat': '0000',
    'smart': '0001',
    'cool': '0010',
    'humid': '0011',
    'fan': '0100'
}
_FORCED_TEMPS = {
    'humid': 23,
    'fan': 23,
    'smart': 23
}


def _get_temp_sensor_part(temperature: int) -> dict:
    return {12: temperature}


def _get_mode_and_temp_set_part(mode: str, temperature: str) -> dict:
    if mode not in _MODES:
        raise ValueError('mode must be one of "heat", "smart", "cool", "humid" or "fan"')
    if not 16 <= temperature <= 30:
        raise ValueError('Temperature must be between 16 and 30 ºC')
    if mode in _FORCED_TEMPS:
        temperature = _FORCED_TEMPS[mode]
    temp_bits = f'{temperature-16:04b}' + _MODES[mode]
    byte_value = int(temp_bits, 2)
    return {3: byte_value}


_FAN_MODES = [
    "auto", "high", "medium_high", "medium", 
    "medium_low",  "low", "turbo", "quiet", "economy"
]

class FanModes:
    auto = "auto"
    high = "high"
    medium_high = "medium_high"
    medium = "medium"
    medium_low = "medium_low"
    low = "low"
    turbo = "turbo"
    quiet = "quiet"
    economy = "economy"


class States:
    on = "on"
    off = "off"


class Modes:
    heat = "heat"
    cool = "cool"
    smart = "smart"
    fan = "fan"
    humid = "humid"


def get_ac_state_message(
    state: str = 'on', 
    fan_mode: str = 'auto',
    mode: [None | str] = None, 
    temperature: [None | str] = None
) -> str:
    if state.lower() == 'off':
        return _codes['off']
    if fan_mode.lower() not in codes:
        raise ValueError(
            f'fan_mode parameter must be one of {", ".join(_FAN_MODES)}'
        )
    base_code = codes.get(fan_mode)
    mode_temp_byte = _get_mode_and_temp_set_part(mode, temperature)
    return cg.get_code(mode_temp_byte, base_code)


def get_ifeel_sensor_message(temperature: int) -> str:
    temp_byte = _get_temp_sensor_part(temperature)
    return cg.get_code(temp_byte, _codes['ifeel'])
