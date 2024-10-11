from flask import Flask,request,jsonify
import os
from werkzeug.utils import secure_filename
import base64

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER): os.makedirs(UPLOAD_FOLDER)

ALLOWED_EXTENSIONS_IMG = {'pnd','jpg','jpeg'}

def allowed_file(filename,allowed_extentions):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in allowed_extentions

@app.route('/upload-img',methods=['POST'])
def upload_img():
    if 'file' not in request.files:
        return jsonify({'error':'file not exists'}),400
    file = request.files['file']

    if file.filename== '':
        return jsonify({'error':'file not select'}),400
    
    if allowed_file(file.filename, ALLOWED_EXTENSIONS_IMG):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'],filename)
        file.save(file_path)

        with open(file_path, 'rb') as img_file:
            encoded_string = base64.b64encode(img_file.read()).decode('utf-8')

        return jsonify({'message':'Image processed', 'base64':encoded_string})
    
    return jsonify({'error':'Unsupported file type'}),400

if __name__ == '__main__':
    app.run(debug=True,port=8181)