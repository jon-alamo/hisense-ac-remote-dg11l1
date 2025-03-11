import importlib.resources
import dg11l1.encoder as encoder
import dg11l1.exceptions as exc
import json
from enum import Enum


BASE_CODES = "base_codes.json"


def get_assets_path() -> str:
    return str(importlib.resources.files("dg11l1.assets") / BASE_CODES)


with open(get_assets_path(), 'r') as f:
    _codes = json.load(f)


_MODES = {
    'heat': '0000',
    'smart': '0001',
    'cool': '0010',
    'dry': '0011',
    'fan': '0100'
}

_FORCED_TEMPS = {
    'humid': 23,
    'fan': 23,
    'smart': 23
}


class BaseEnum(Enum):

    @classmethod
    def values(cls):
        return [e.value for e in cls]

    @classmethod
    def names(cls):
        return [e.name for e in cls]


class FanModes(BaseEnum):
    name = "fan_mode"
    auto = "auto"
    high = "high"
    medium_high = "medium_high"
    medium = "medium"
    medium_low = "medium_low"
    low = "low"
    turbo = "turbo"
    quiet = "quiet"
    economy = "economy"


class States(BaseEnum):
    name = "state"
    on = "on"
    off = "off"


class Modes(BaseEnum):
    name = "mode"
    heat = "heat"
    cool = "cool"
    smart = "smart"
    fan = "fan"
    humid = "dry"


class Ranges(BaseEnum):
    ifeel = [0, 37]
    control = [16, 31]


def validate_parameters(
        state: str = None,
        fan_mode: str = None,
        mode: str = None,
        temperature: int = None,
        ifeel_temp: int = None
):
    if state is not None and state not in States.values():
        raise exc.InvalidValue(States)
    if fan_mode is not None and fan_mode not in _codes:
        raise exc.InvalidValue(FanModes)
    if mode is not None and mode not in Modes.values():
        raise exc.InvalidValue(Modes)
    if temperature is not None and temperature not in range(*Ranges.control.value):
        raise exc.InvalidTemperature('control', Ranges.control.value)
    if ifeel_temp is not None and ifeel_temp not in range(*Ranges.ifeel.value):
        raise exc.InvalidTemperature('ifeel', Ranges.ifeel.value)


def _get_temp_sensor_part(temperature: int) -> dict:
    return {12: temperature}


def _get_mode_and_temp_set_part(mode: str, temperature: int) -> dict:
    if mode in _FORCED_TEMPS:
        temperature = _FORCED_TEMPS[mode]
    temp_bits = f'{temperature-16:04b}' + _MODES[mode]
    byte_value = int(temp_bits, 2)
    return {3: byte_value}


def get_state_message(state: str):
    validate_parameters(state=state)
    return encoder.compose_message({}, _codes['off'])


def get_ifeel_sensor_message(
        ifeel_temp: int,
) -> list[int] | bytes:
    validate_parameters(ifeel_temp=ifeel_temp)
    temp_byte = _get_temp_sensor_part(ifeel_temp)
    message = encoder.compose_message(temp_byte, _codes['ifeel'])
    return message


def get_operation_mode_message(
        fan_mode: str,
        mode: str,
        temperature: int,
) -> list[int] | bytes:
    validate_parameters(fan_mode=fan_mode, mode=mode, temperature=temperature)
    base_code = _codes[fan_mode]
    mode_temp_part = _get_mode_and_temp_set_part(mode, temperature)
    message = encoder.compose_message(mode_temp_part, base_code)
    return message


def get_remote_action_message(
        state: str = None,
        ifeel_temp: int = None,
        fan_mode: str = None,
        mode: str = None,
        temperature: int = None
):
    if state is not None:
        message = get_state_message(state)
    elif ifeel_temp is not None:
        message = get_ifeel_sensor_message(ifeel_temp)
    elif fan_mode is not None and mode is not None and temperature is not None:
        message = get_operation_mode_message(
            fan_mode, mode, temperature
        )
    else:
        raise ValueError('Invalid parameters')
    return message


def get_remote_action_message_b64(
        state: str = None,
        ifeel_temp: int = None,
        fan_mode: str = None,
        mode: str = None,
        temperature: int = None
):
    return encoder.b64_message(get_remote_action_message(
        state=state,
        ifeel_temp=ifeel_temp,
        fan_mode=fan_mode,
        mode=mode,
        temperature=temperature
    ))
