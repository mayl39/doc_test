from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import os
from models import db, Document

UPLOAD_FOLDER = 'uploads/'
ALLOWED_EXTENSIONS = {'pdf', 'docx', 'xlsx'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file part"

    file = request.files['file']
    if file.filename == '':
        return "No selected file"

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        new_doc = Document(filename=filename, filepath=filepath, status='pending')
        db.session.add(new_doc)
        db.session.commit()

        return redirect(url_for('upload_success'))
    
@app.route('/documents', methods=['GET'])
def list_documents():
    category = request.args.get('category')
    subcategory = request.args.get('subcategory')
    status = request.args.get('status')

    query = Document.query
    if category:
        query = query.filter_by(category_id=category)
    if subcategory:
        query = query.filter_by(subcategory_id=subcategory)
    if status:
        query = query.filter_by(status=status)

    documents = query.all()
    return render_template('documents.html', documents=documents)
