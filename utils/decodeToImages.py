import base64

def decode_base64_to_image(base64_string, output_path):
    try:
        with open(output_path, "wb") as f:
            f.write(base64.b64decode(base64_string))
        return True
    except Exception as e:
        print(f"Error decoding image: {e}")
        return False