from flask import Flask, request, jsonify
import os
from werkzeug.utils import secure_filename
from moviepy.editor import VideoFileClip

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

ALLOWED_EXTENSIONS = {'mp4,mkv'}

if not os.path.exists(UPLOAD_FOLDER): os.makedirs(UPLOAD_FOLDER)

@app.route('/upload-video', methods=['POST'])
def upload_video():
    if 'file' not in request.files:
        return jsonify({'errror':'file not exists'}),400
    file = request.files['file']

    if file.filename == '':
        return jsonify({'errror':'file not select'}),400
    
    if file:
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)
            try:
                video = VideoFileClip(file_path)
                duration = video.duration
                video.close()
                return jsonify({'filename':file.filename, 'duration':duration}),200
            except Exception as e:
                return jsonify({'error':str(e)}),500
    return jsonify({'error':'Unsupported file type'})
    
if __name__ == '__main__':
    app.run("0.0.0.0", debug=True, port=8585)