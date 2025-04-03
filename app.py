import pyodbc
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# ตั้งค่าการเชื่อมต่อกับ Azure SQL
server = 'documentupdown.database.windows.net'
database = 'DocumentManagement'
username = 'maythawee'
password = 'Maymys@393833'
driver = '{ODBC Driver 17 for SQL Server}'

app.config['SQLALCHEMY_DATABASE_URI'] = f'mssql+pyodbc://{username}:{password}@{server}/{database}?driver={driver}'

db = SQLAlchemy(app)

class Document(db.Model):
    __tablename__ = 'Documents'
    DocumentID = db.Column(db.Integer, primary_key=True)
    FileName = db.Column(db.String(255))
    FilePath = db.Column(db.String(500))
    Category = db.Column(db.String(50))
    SubCategory = db.Column(db.String(50))
    Status = db.Column(db.String(20))
    UploadDate = db.Column(db.DateTime)
    UploadedBy = db.Column(db.String(100))

# หน้าแรก
@app.route('/')
def index():
    documents = Document.query.all()
    return render_template('index.html', documents=documents)

# ฟอร์มอัพโหลดเอกสาร
@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files['document']
        category = request.form['category']
        subcategory = request.form['subcategory']
        status = request.form['status']
        uploaded_by = request.form['uploaded_by']

        if file:
            filename = file.filename
            filepath = os.path.join('uploads', filename)
            file.save(filepath)

            new_doc = Document(FileName=filename, FilePath=filepath, Category=category, SubCategory=subcategory, Status=status, UploadedBy=uploaded_by)
            db.session.add(new_doc)
            db.session.commit()
            return redirect(url_for('index'))
    return render_template('upload.html')

# หน้าแสดงเอกสารและดาวน์โหลด
@app.route('/download/<int:document_id>')
def download(document_id):
    doc = Document.query.get_or_404(document_id)
    return send_file(doc.FilePath, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
