import broadlink as blk
import base64


def get_device(ip):
    device = blk.hello(ip)
    device.auth()
    return device


def send_b64code(device, b64code):
    byte_code = base64.b64decode(b64code.encode('utf-8'))
    return device.send_data(byte_code)

