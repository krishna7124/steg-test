from cryptography.fernet import Fernet

def encrypt_message(message, key):
    fernet = Fernet(key)
    return fernet.encrypt(message.encode())

def decrypt_message(encrypted_message, key):
    fernet = Fernet(key)
    return fernet.decrypt(encrypted_message).decode()

def encode_text(base_text, secret_message, key):
    encrypted_message = encrypt_message(secret_message, key)
    binary_message = ''.join(format(byte, '08b') for byte in encrypted_message)
    encoded_text = base_text + ''.join(['\u200b' if bit == '1' else '\u200c' for bit in binary_message])
    return encoded_text

def decode_text(encoded_text, key):
    binary_message = ''.join(['1' if char == '\u200b' else '0' for char in encoded_text if char in '\u200b\u200c'])
    encrypted_message = bytes(int(binary_message[i:i+8], 2) for i in range(0, len(binary_message), 8))
    return decrypt_message(encrypted_message, key)
