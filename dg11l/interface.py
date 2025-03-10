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
    message = features.get_remote_action_message(
        state=state,
        ifeel_temp=ifeel_temp,
        fan_mode=fan_mode,
        mode=mode,
        temperature=temperature
    )
    return device.send_data(message)
