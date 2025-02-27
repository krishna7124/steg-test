import streamlit as st
import streamlit.components.v1 as components
from cryptography.fernet import Fernet
from modules import text_steganography as text_steg, image_steganography as img_steg, audio_steganography as audio_steg
from PIL import Image

# ✅ Set browser tab title & icon
st.set_page_config(page_title="Steganography Tool", page_icon="🔒", layout="wide")

def copy_to_clipboard_button(text_to_copy, button_label):
    """Renders a button to copy text to the clipboard."""
    custom_js = f"""
    <script>
        function copyToClipboard(text) {{
            navigator.clipboard.writeText(text).then(function() {{
                alert("Copied to clipboard!");
            }}, function(err) {{
                alert("Failed to copy text: " + err);
            }});
        }}
    </script>
    <button onclick="copyToClipboard('{text_to_copy}')" style="
        background-color: #4CAF50;
        color: white;
        border: none;
        padding: 10px 15px;
        font-size: 14px;
        border-radius: 5px;
        cursor: pointer;
        margin-top: 10px;">{button_label}</button>
    """
    components.html(custom_js, height=50)

def main():
    st.title("🔒 Steganography Tool")

    # Sidebar for choosing encoding/decoding type
    option = st.sidebar.selectbox("Select Steganography Type", ("Text", "Audio", "Image"))

    # ✅ Define `action` before using it
    action = st.radio("Choose Action", ("Encode", "Decode"))

    # ✅ Ensure all options correctly use `action`
    if option == "Text":
        st.header("📜 Text Steganography")

        if action == "Encode":
            st.subheader("Encoding Text")
            message = st.text_area("Enter the message to encode", "")
            base_text = st.text_area("Enter the base text", "")

            if st.button("Encode"):
                key = Fernet.generate_key()
                encoded_text = text_steg.encode_text(base_text, message, key)
                
                st.success("✅ Encoded Text:")
                st.code(encoded_text)

        elif action == "Decode":
            st.subheader("🔓 Decoding Text")
            encoded_message = st.text_area("Enter the encoded text", "")
            key_input = st.text_input("Enter Encryption Key (for decoding)", "")

            if st.button("Decode") and key_input:
                try:
                    decoded_message = text_steg.decode_text(encoded_message, key_input.encode())
                    st.success("🔍 Decoded Message:")
                    st.code(decoded_message)
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")

    elif option == "Audio":
        st.header("🎵 Audio Steganography")

        if action == "Encode":
            st.subheader("Encoding Audio")
            message = st.text_area("Enter the message to encode", "")
            audio_file = st.file_uploader("Choose an audio file", type=["wav", "mp3"])

            if audio_file and st.button("Encode"):
                key = Fernet.generate_key()
                output_audio = "encoded_audio.wav"

                # ✅ Handle uploaded audio correctly
                temp_audio_path = f"temp_{audio_file.name}"
                with open(temp_audio_path, "wb") as f:
                    f.write(audio_file.getbuffer())

                audio_steg.encode_audio(temp_audio_path, message, key, output_audio)

                st.success("✅ Audio successfully encoded!")
                st.code(key.decode())

        elif action == "Decode":
            st.subheader("Decoding Audio")
            audio_file = st.file_uploader("Choose an encoded audio file", type=["wav"])
            key_input = st.text_input("Enter Encryption Key (for decoding)", "")

            if audio_file and st.button("Decode") and key_input:
                with open(audio_file.name, "wb") as f:
                    f.write(audio_file.getbuffer())

                try:
                    decoded_message = audio_steg.decode_audio(audio_file.name, key_input.encode())
                    st.success("🔍 Decoded Message:")
                    st.code(decoded_message)
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")

    elif option == "Image":
        st.header("🖼 Image Steganography")

        if action == "Encode":
            st.subheader("Encoding Image")
            message = st.text_area("Enter the message to encode", "")
            image_file = st.file_uploader("Choose an image file", type=["png", "jpg", "jpeg"])

            if image_file and st.button("Encode"):
                key = Fernet.generate_key()
                output_image = "encoded_image.png"

                img = Image.open(image_file).convert("RGB")
                stego_image = img_steg.encode_image(img, message, key)
                stego_image.save(output_image)

                st.success("✅ Image successfully encoded!")
                st.code(key.decode())

        elif action == "Decode":
            st.subheader("Decoding Image")
            image_file = st.file_uploader("Choose an encoded image file", type=["png", "jpg", "jpeg"])
            key_input = st.text_input("Enter Encryption Key (for decoding)", "")

            if image_file and st.button("Decode") and key_input:
                img = Image.open(image_file).convert("RGB")

                try:
                    decoded_message = img_steg.decode_image(img, key_input.encode())
                    st.success("🔍 Decoded Message:")
                    st.code(decoded_message)
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    main()
