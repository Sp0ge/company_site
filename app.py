from flask import Flask , render_template, url_for, request
from flask_sqlalchemy import SQLAlchemy 

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sql_database.db'
db = SQLAlchemy(app)
app.secret_key='Lk2kIC1X1RpyJSkMqAfJJltF4JkUidId4S3cpmuzxmyyxjZw6IR17Ac75tA6XNS5HDtZKRHbDaQ9zHw8V2jMSaPGfSKO2dEnif63'
last = ""


@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="80", debug=True) 
    db.create_all()