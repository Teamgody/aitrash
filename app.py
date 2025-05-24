import os
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
from PIL import Image
import numpy as np

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# 🔸 ฟังก์ชันวิเคราะห์สีภาพแล้วแยกประเภทขยะ + รูปถังขยะ
def classify_by_color(image_path):
    img = Image.open(image_path).resize((100, 100)).convert('RGB')
    pixels = np.array(img).reshape(-1, 3)
    avg_brightness = np.mean(pixels)

    if avg_brightness < 60:
        return "ขยะอินทรีย์ ", "bins/organic.png"
    elif avg_brightness < 140:
        return "ขยะทั่วไป", "bins/general.png"
    elif avg_brightness < 100:
        return "ขยะรีไซเคิล ", "bins/recycle.png"
    else:
        return "ขยะรีไซเคิล ", "bins/metal.png"

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    bin_image = None

    if request.method == 'POST':
        file = request.files['image']
        if file:
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            result, bin_image = classify_by_color(filepath)

    return render_template('index.html', result=result, bin_image=bin_image)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
