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

    # Sidebar selection
    option = st.sidebar.selectbox("🔍 Select Steganography Type", ("Text", "Audio", "Image"))
    action = st.radio("Choose Action", ("Encode", "Decode"))

    # 🔹 TEXT STEGANOGRAPHY
    if option == "Text":
        st.header("📜 Text Steganography")

        if action == "Encode":
            st.subheader("🛠 Encoding Text")
            message = st.text_area("Enter the message to encode", "")
            base_text = st.text_area("Enter the base text", "")

            if st.button("Encode"):
                key = Fernet.generate_key()
                encoded_text = text_steg.encode_text(base_text, message, key)

                st.success("✅ Encoded Text:")
                st.code(encoded_text)
                copy_to_clipboard_button(encoded_text, "Copy Encoded Message")

                st.write("🔑 Encryption Key for Decoding:")
                st.code(key.decode())
                copy_to_clipboard_button(key.decode(), "Copy Key")

        elif action == "Decode":
            st.subheader("🔓 Decoding Text")
            encoded_message = st.text_area("Enter the encoded text", "")
            key_input = st.text_input("Enter Encryption Key (for decoding)", "")

            if st.button("Decode"):
                if key_input:
                    try:
                        decoded_message = text_steg.decode_text(encoded_message, key_input.encode())
                        st.success("🔍 Decoded Message:")
                        st.code(decoded_message)
                        copy_to_clipboard_button(decoded_message, "Copy Decoded Message")
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")
                else:
                    st.error("⚠️ Please provide the encryption key for decoding.")

    # 🔹 AUDIO STEGANOGRAPHY
    elif option == "Audio":
        st.header("🎵 Audio Steganography")

        if action == "Encode":
            st.subheader("🛠 Encoding Audio")
            message = st.text_area("Enter the message to encode", "")
            audio_file = st.file_uploader("Choose an audio file", type=["wav", "mp3"])

            if audio_file and st.button("Encode"):
                key = Fernet.generate_key()
                output_audio = "encoded_audio.wav"

                # ✅ Process and save uploaded audio
                with open(audio_file.name, "wb") as f:
                    f.write(audio_file.getbuffer())

                # ✅ Call encode_audio function
                audio_steg.encode_audio(audio_file.name, message, key, output_audio)

                st.success("✅ Audio successfully encoded!")
                st.write("🔑 Encryption Key for Decoding:")
                st.code(key.decode())
                copy_to_clipboard_button(key.decode(), "Copy Key")

                with open(output_audio, "rb") as file:
                    st.download_button(label="📥 Download Encoded Audio", data=file, file_name=output_audio, mime="audio/wav")

        elif action == "Decode":
            st.subheader("🔓 Decoding Audio")
            audio_file = st.file_uploader("Choose an encoded audio file", type=["wav"])
            key_input = st.text_input("Enter Encryption Key (for decoding)", "")

            if audio_file and st.button("Decode"):
                if key_input:
                    with open(audio_file.name, "wb") as f:
                        f.write(audio_file.getbuffer())

                    try:
                        decoded_message = audio_steg.decode_audio(audio_file.name, key_input.encode())
                        st.success("🔍 Decoded Message:")
                        st.code(decoded_message)
                        copy_to_clipboard_button(decoded_message, "Copy Decoded Message")
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")
                else:
                    st.error("⚠️ Please provide the encryption key for decoding.")

    # 🔹 IMAGE STEGANOGRAPHY
    elif option == "Image":
        st.header("🖼 Image Steganography")

        if action == "Encode":
            st.subheader("🛠 Encoding Image")
            message = st.text_area("Enter the message to encode", "")
            image_file = st.file_uploader("Choose an image file", type=["png", "jpg", "jpeg"])

            if image_file and st.button("Encode"):
                key = Fernet.generate_key()
                output_image = "encoded_image.png"

                # ✅ Convert uploaded file to PIL Image
                img = Image.open(image_file).convert("RGB")

                # ✅ Call encode_image with PIL Image object
                stego_image = img_steg.encode_image(img, message, key)

                # ✅ Save the modified image
                stego_image.save(output_image)

                st.success("✅ Image successfully encoded!")
                st.write("🔑 Encryption Key for Decoding:")
                st.code(key.decode())
                copy_to_clipboard_button(key.decode(), "Copy Key")

                with open(output_image, "rb") as file:
                    st.download_button(label="📥 Download Encoded Image", data=file, file_name=output_image, mime="image/png")

        elif action == "Decode":
            st.subheader("🔓 Decoding Image")
            image_file = st.file_uploader("Choose an encoded image file", type=["png", "jpg", "jpeg"])
            key_input = st.text_input("Enter Encryption Key (for decoding)", "")

            if image_file and st.button("Decode"):
                if key_input:
                    img = Image.open(image_file).convert("RGB")

                    try:
                        decoded_message = img_steg.decode_image(img, key_input.encode())
                        st.success("🔍 Decoded Message:")
                        st.code(decoded_message)
                        copy_to_clipboard_button(decoded_message, "Copy Decoded Message")
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")
                else:
                    st.error("⚠️ Please provide the encryption key for decoding.")

if __name__ == "__main__":
    main()
