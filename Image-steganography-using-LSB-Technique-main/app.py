from flask import Flask, render_template, request, send_file
from stegano import lsb
import os

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['DOWNLOAD_FOLDER'] = 'downloads'

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['DOWNLOAD_FOLDER'], exist_ok=True)

def embed_message(input_image_path, text):
    output_image_path = os.path.join(app.config['DOWNLOAD_FOLDER'], 'embedded_image.png')
    secret_message = lsb.hide(input_image_path, text)
    secret_message.save(output_image_path)
    return output_image_path

def extract_message(image_path):
    try:
        extracted_message = lsb.reveal(image_path)
        return extracted_message
    except IndexError:
        return ""

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/embed', methods=['POST'])
def embed():
    embedded_image = None

    if request.method == 'POST':
        uploaded_file = request.files.get('image_file')
        text = request.form['secret_message']

        if uploaded_file:
            filename = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)
            uploaded_file.save(filename)

            embedded_image = embed_message(filename, text)

    if embedded_image:
        return send_file(embedded_image, as_attachment=True)
    else:
        return "Error embedding message"

@app.route('/extract', methods=['POST'])
def extract():
    if request.method == 'POST':
        uploaded_file = request.files.get('image_file')

        if uploaded_file:
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)
            uploaded_file.save(image_path)
            extracted_message = extract_message(image_path)
            print(extract_message)
  
    if not extracted_message or not extracted_message.isprintable():
        return " "

    return f"{extracted_message}"

if __name__ == '__main__':
    app.run(debug=True)