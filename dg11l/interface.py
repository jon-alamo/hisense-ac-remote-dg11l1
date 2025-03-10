import broadlink as blk
import base64

import dg11l.features as features


def get_device(ip):
    device = blk.hello(ip)
    device.auth()
    return device


def send_b64code(device, b64code):
    byte_code = base64.b64decode(b64code.encode('utf-8'))
    return device.send_data(byte_code)


def send_remote_action(
        device: blk.Device,
        state: str = None,
        ifeel_temp: int = None,
        fan_mode: str = None,
        mode: str = None,
        temperature: int = None
):
    if state is not None:
        message = features.get_state_message(state)
    elif ifeel_temp is not None:
        message = features.get_ifeel_sensor_message(ifeel_temp)
    elif fan_mode is not None and mode is not None and temperature is not None:
        message = features.get_operation_mode_message(
            fan_mode, mode, temperature
        )
    else:
        raise ValueError('Invalid parameters')
    return device.send_data(message)
