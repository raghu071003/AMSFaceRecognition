from flask import Flask, redirect, render_template, request, jsonify,session, url_for
import os
import face_recognition

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
REFERENCE_FOLDER = 'referenceImages'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

if not os.path.exists('uploads'):
    os.makedirs('uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def load_reference_images(folder_path):
    reference_encodings = []
    reference_names = []

    for filename in os.listdir(folder_path):
        image_path = os.path.join(folder_path, filename)
        if os.path.isfile(image_path):
            image = face_recognition.load_image_file(image_path)
            encoding = face_recognition.face_encodings(image)[0]
            reference_encodings.append(encoding)
            reference_names.append(filename)

    return reference_encodings, reference_names

def detect_faces_and_compare(target_image_path, reference_encodings, reference_names):
    target_image = face_recognition.load_image_file(target_image_path)
    face_locations = face_recognition.face_locations(target_image)
    target_encodings = face_recognition.face_encodings(target_image, face_locations)

    matched_images = []
    unmatched_count = 0

    for target_encoding in target_encodings:
        matches = face_recognition.compare_faces(reference_encodings, target_encoding)
        if any(matches):
            matched_index = matches.index(True)
            matched_images.append(reference_names[matched_index])
        else:
            unmatched_count += 1

    return matched_images, unmatched_count

users = {
    'user1': {'username': 'faculty', 'password': 'faculty'}
}
app.secret_key = 'your_secret_key_here'
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        print(username,password)
        if username == 'faculty' and 'faculty' == password:
            session['username'] = username
            return redirect(url_for('index'))
        else:
            return 'Invalid username or password'
    return render_template('login.html')
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process_image():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"})

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"})

    if file and allowed_file(file.filename):
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)

        reference_folder = os.path.join(os.getcwd(), REFERENCE_FOLDER)
        reference_encodings, reference_names = load_reference_images(reference_folder)

        matched_images, unmatched_count = detect_faces_and_compare(file_path, reference_encodings, reference_names)

        return jsonify({
            "matched_images": matched_images,
            "unmatched_count": unmatched_count
        })
    else:
        return jsonify({"error": "File type not allowed"})

if __name__ == '__main__':
    app.run(debug=True)
