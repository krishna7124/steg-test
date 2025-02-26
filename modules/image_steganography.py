from PIL import Image
import numpy as np
from cryptography.fernet import Fernet

def encrypt_message(message, key):
    fernet = Fernet(key)
    return fernet.encrypt(message.encode())

def decrypt_message(encrypted_message, key):
    fernet = Fernet(key)
    return fernet.decrypt(encrypted_message).decode()

def message_to_binary(message):
    return ''.join(format(byte, '08b') for byte in message)

def binary_to_message(binary):
    bytes_data = [binary[i:i+8] for i in range(0, len(binary), 8)]
    return bytes(int(byte, 2) for byte in bytes_data)

def encode_image(image_path, message, key):
    img = Image.open(image_path)
    data = np.array(img)
    encrypted_message = encrypt_message(message, key)
    binary_message = message_to_binary(encrypted_message) + '1111111111111110'
    flat_data = data.flatten()

    for i, bit in enumerate(binary_message):
        flat_data[i] = (flat_data[i] & ~1) | int(bit)

    new_data = flat_data.reshape(data.shape)
    stego_img = Image.fromarray(new_data)
    return stego_img

def decode_image(image_path, key):
    img = Image.open(image_path)
    data = np.array(img).flatten()
    binary_message = ''.join(str(bit & 1) for bit in data)
    end_marker = '1111111111111110'
    if end_marker in binary_message:
        binary_message = binary_message[:binary_message.index(end_marker)]

    encrypted_message = binary_to_message(binary_message)
    return decrypt_message(encrypted_message, key)
