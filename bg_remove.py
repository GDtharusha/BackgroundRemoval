from flask import Flask, request, jsonify
from rembg import remove
from PIL import Image
from io import BytesIO
import base64

app = Flask(__name__)

def convert_image_to_base64(img):
    buf = BytesIO()
    img.save(buf, format="PNG")
    byte_im = buf.getvalue()
    base64_encoded = base64.b64encode(byte_im).decode('utf-8')
    return base64_encoded

def convert_base64_to_image(base64_str):
    img_data = base64.b64decode(base64_str)
    img = Image.open(BytesIO(img_data))
    return img

@app.route('/remove-background', methods=['POST'])
def remove_background():
    data = request.get_json()

    if 'image' not in data:
        return jsonify({'error': 'No image data provided'}), 400

    try:
        image = convert_base64_to_image(data['image'])
        fixed = remove(image)
        fixed_base64 = convert_image_to_base64(fixed)
        return jsonify({'fixed_image': fixed_base64}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
