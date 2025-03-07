from functools import reduce
import base64

RAW_INIT = [38, 0, 92, 1, 0, 1, 29, 144]
RAW_END = [20, 0, 13, 5]

ZERO_TIME = 20
ONE_TIME = 55
EMPTY_TIME = 20
SEGMENT_SEP_SEQ = [EMPTY_TIME, 255]
SEGMENT_SEP_POSITIONS = [104, 234]


def get_xor(byte_list):
    return reduce(lambda x, y: x ^ y, byte_list)


def integers_to_bits(integers):
    return [format(b, '08b') for b in integers]


def reverse_bits_in_byte_sequence(bytes_sequence):
    return [b[::-1] for b in bytes_sequence]


def concat_bits(bytes_sequence):
    return reduce(lambda x, y: x + y, bytes_sequence)


def serialize_bits_to_raw_format(bits):
    raw_bits = []
    for bit in bits:
        raw_bits.append(EMPTY_TIME)
        raw_bits.append(ZERO_TIME if bit == '0' else ONE_TIME)
    return raw_bits


def format_raw_bits_sequence(raw_bits):
    raw_bits = RAW_INIT + raw_bits + RAW_END
    for i in SEGMENT_SEP_POSITIONS:
        raw_bits = raw_bits[:i] + SEGMENT_SEP_SEQ + raw_bits[i:]
    return raw_bits


def encode_message(bits):
    return base64.b64encode(bytes(bits))


def get_code(input_bytes: dict, base_code: list) -> str:
    ''' Method to generate a hisense ac controller code based on a base_code
    and passing function's data bytes.
    :param input_butes: dict: key/value pairs representing byte position and value respectively.
    :param base_code: str: name of the base code which will be used for the content of the bytes
    not passed within the input_bytes dictionary.
    '''
    for position, data in input_bytes.items():
        base_code[position] = data
    base_code[13] = get_xor(base_code[2:13])
    byte_bits = integers_to_bits(base_code)
    lsb_first_bytes = reverse_bits_in_byte_sequence(byte_bits)
    lsb_first_bits = concat_bits(lsb_first_bytes)
    raw_bits_data = serialize_bits_to_raw_format(lsb_first_bits)
    raw_bits = format_raw_bits_sequence(raw_bits_data)
    return encode_message(raw_bits)

