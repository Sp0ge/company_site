from flask import Flask,render_template,url_for,request,redirect,flash
from flask_login import login_user,logout_user,current_user,login_required,LoginManager
from datetime import datetime,time
import time
import threading
from flask_talisman import Talisman
from flask_sslify import SSLify
from flask_recaptcha import ReCaptcha
from flask_sqlalchemy import SQLAlchemy 


app = Flask(__name__, static_folder="static", static_url_path="/static")
Talisman(app)
sslify = SSLify(app)
app.config['RECAPTCHA_SITE_KEY'] = '6LeGuVMgAAAAALJqOYDubfEMMPQLZl68jriPo7Aq'
app.config['RECAPTCHA_SECRET_KEY'] = '6LeGuVMgAAAAAGqbYmntFNWZaE5QC57mlLO71CIB'
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/database.db'
db = SQLAlchemy(app)
recaptcha = ReCaptcha(app)
app.secret_key='Lk2kIC1X1RpyJSkMqAfJJltF4JkUidId4S3cpmuzxmyyxjZw6IR17Ac75tA6XNS5HDtZKRHbDaQ9zHw8V2jMSaPGfSKO2dEnif63'
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'admin_login'



class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    
    def is_active(self):
        return True
    
    def get_id(self):
        return str(self.id)
    def is_authenticated(self):
        return True
    
    def __repr__ (self):
        return f"User('{self.username}')"
    
class Mail_request(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False)
    email = db.Column(db.String(60), nullable=False)
    text = db.Column(db.Text, nullable=False)
    tel = db.Column(db.String(60), nullable=False)
    subject = db.Column(db.String(60), nullable=False)
    client = db.Column(db.String(60), nullable=False)
    date = db.Column(db.DateTime, default=datetime.now())
    def __repr__ (self):
        return '<Mail_request %r>' % self.id


@login_manager.user_loader
def load_user(user_id):
    return db.session.query(User).get(user_id)

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', year=datetime.now().year ,title="Главная")

@app.route('/req')
def req():
    return render_template('req.html', year=datetime.now().year ,title="Заявка")

@app.route('/admin_login', methods=['GET','POST'])
def admin_login():
    if current_user.is_authenticated:
        return redirect(url_for("control_panel"))
    if request.method == 'POST':
        ip = request.remote_addr
        user = request.form['username']
        password = request.form['password']
        password.replace(' ', '')
        logtime = datetime.now()
        print(f"\n \n User: {user} is logging in control page from IP: {ip} -- {logtime} \n \n")
        user = User.query.filter_by(username=user).first()
        password = User.query.filter_by(password=password).first()
        if not user or not password:
            return 'Invalid username or password'
        else:
            usr = db.session.query(User).first()
            login_user(usr)
            return redirect(url_for("control_panel"))
   
    return render_template('admin_login.html')

@app.route('/control_panel',methods=['POST','GET'])
@login_required
def control_panel():
    mails = Mail_request.query.all()
    return render_template('control_panel.html',mails=mails,title="Admin Панель")

@app.route('/mail_request',methods=['POST','GET'])
def mail_request():
    if request.method == "POST":
        if recaptcha.verify():
            name = request.form['name']
            email = request.form['email']
            text = request.form['message']
            tel = request.form['tel']
            subject = request.form['subject']
            client = request.form['client']
            mail_request = Mail_request(name=name,subject=subject,client=client,tel=tel,email=email,text=text)
            try:
                db.session.add(mail_request)
                db.session.commit()
                return redirect('/home')
            except:
                return 'Ошибка Формы'
        else:
            return redirect("/req")

    else:
        return redirect("/req")

@app.route('/mail/<int:id>/del')
@login_required
def mail_delete(id):
    try:
        delid = Mail_request.query.get_or_404(id)
        db.session.delete(delid)
        db.session.commit()
        return redirect(url_for('control_panel'))
    except:
        return 'Ошибка формы удалния почты'

@app.errorhandler(404)
def not_found(e):
    return render_template("404.html", title="404")

@app.errorhandler(500)
def Server_error(e):
    return render_template("500.html", title="500")

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))





def hs():
    context=('ssl/cert.crt','ssl/key.pem')
    app.run(
        port=443,
        ssl_context=context,
        debug=development_mode,
        host ='0.0.0.0',
        use_reloader=False
        )
    
def hp():
    app.run(
        port=80,
        debug=development_mode,
        host ='0.0.0.0',
        use_reloader=False
        )

if __name__ == "__main__":
    db.create_all()
    global development_mode
    development_mode = True    
    y = threading.Thread(target=hp)
    x = threading.Thread(target=hs)
    y.start()
    time.sleep(2)
    x.start()