import base64
import json

R_ZERO = 17
R_ONE = 56
MARGIN = 5

RAW_CODES = 'dg11l1/assets/smartir_codes.json'

with open(RAW_CODES, 'r') as f:
    raw_codes = json.load(f)


def get_bytes_from_b64(b64_message: str) -> bytes:
    return base64.b64decode(b64_message.encode('utf-8'))


def get_raw_message_from_bytes(bytes_message: bytes) -> list:
    return [int(b) for b in bytes_message]


def get_normalized_value(value: int) -> int:
    if R_ZERO-MARGIN <= value <= R_ZERO+MARGIN:
        return 0
    elif R_ONE-MARGIN <= value <= R_ONE+MARGIN:
        return 1
    else:
        return -1


def normalize_raw_message(raw_message: list) -> list:
    return list(map(get_normalized_value, raw_message))


def extract_meaning_values(normalized_message: list):
    meaning_message = normalized_message.copy()
    first_zero = normalized_message.index(0)
    sign = -1
    for i, value in enumerate(meaning_message):
        if i < first_zero:
            continue
        if sign == -1:
            meaning_message[i] = sign
        sign *= -1
    return [v for v in meaning_message if v != -1]


def deserialize_bit_sequence(meaning_message: list):
    byte_seq = []
    byte_bits = ''
    for i, bit in enumerate(meaning_message):
        byte_bits += str(bit)
        if (i+1) % 8 == 0:
            byte_seq.append(byte_bits)
            byte_bits = ''
    return byte_seq


def reverse_bits_in_byte_sequence(byte_seq: list):
    return [b[::-1] for b in byte_seq]


def convert_to_integers(reversed_bytes):
    return [int(b, 2) for b in reversed_bytes]


def decode_b64_message(b64_message):
    bytes_message = get_bytes_from_b64(b64_message)
    raw_message = get_raw_message_from_bytes(bytes_message)
    normalized_message = normalize_raw_message(raw_message)
    meaning_values = extract_meaning_values(normalized_message)
    byte_sequence = deserialize_bit_sequence(meaning_values)
    reversed_bits = reverse_bits_in_byte_sequence(byte_sequence)
    return convert_to_integers(reversed_bits)
