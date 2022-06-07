from flask import Flask , render_template, url_for, request
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy 

app = Flask(__name__)
db = SQLAlchemy(app)
app.secret_key='Lk2kIC1X1RpyJSkMqAfJJltF4JkUidId4S3cpmuzxmyyxjZw6IR17Ac75tA6XNS5HDtZKRHbDaQ9zHw8V2jMSaPGfSKO2dEnif63'

@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html', year=datetime.now().year ,title="Главная")

@app.route('/about')
def about():
    return render_template('about.html', year=datetime.now().year ,title="О нас")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="80", debug=True) 
