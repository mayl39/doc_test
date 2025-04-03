from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import SQLALCHEMY_DATABASE_URI

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI

db = SQLAlchemy(app)

@app.route("/")
def home():
    return "Connected to Azure SQL Database!"

if __name__ == "__main__":
    app.run(debug=True)
