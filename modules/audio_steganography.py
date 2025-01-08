from pydub import AudioSegment
import wave
from cryptography.fernet import Fernet

# Encrypt the message
def encrypt_message(message, key):
    fernet = Fernet(key)
    return fernet.encrypt(message.encode())

# Decrypt the message
def decrypt_message(encrypted_message, key):
    fernet = Fernet(key)
    return fernet.decrypt(encrypted_message).decode()

# Convert audio to WAV
def convert_to_wav(input_audio_path, output_wav_path):
    audio = AudioSegment.from_file(input_audio_path)
    audio.export(output_wav_path, format="wav")

# Encode message into audio
def encode_audio(input_audio_path, message, key, output_audio_path):
    if not input_audio_path.name.endswith('.wav'):
        temp_wav_path = "temp.wav"
        convert_to_wav(input_audio_path, temp_wav_path)
        input_audio_path = temp_wav_path

    encrypted_message = encrypt_message(message, key)
    binary_message = ''.join(format(byte, '08b') for byte in encrypted_message) + '1111111111111110'

    with wave.open(input_audio_path, 'rb') as audio:
        params = audio.getparams()
        frames = bytearray(list(audio.readframes(audio.getnframes())))

    for i, bit in enumerate(binary_message):
        frames[i] = (frames[i] & ~1) | int(bit)

    with wave.open(output_audio_path, 'wb') as stego_audio:
        stego_audio.setparams(params)
        stego_audio.writeframes(bytes(frames))

# Decode message from audio
def decode_audio(stego_audio_path, key):
    with wave.open(stego_audio_path, 'rb') as audio:
        frames = bytearray(list(audio.readframes(audio.getnframes())))

    binary_message = ''.join(str(frame & 1) for frame in frames)
    end_marker = '1111111111111110'
    if end_marker in binary_message:
        binary_message = binary_message[:binary_message.index(end_marker)]

    encrypted_message = bytes(int(binary_message[i:i+8], 2) for i in range(0, len(binary_message), 8))
    return decrypt_message(encrypted_message, key)
