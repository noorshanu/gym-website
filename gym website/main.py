from flask import Flask, render_template, request,session,logging,url_for,redirect,flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import scoped_session,sessionmaker
from passlib.hash import sha256_crypt 
from flask_login import LoginManager

from flask_mail import Mail
import json
from datetime import datetime




with open('config.json', 'r') as c:
    params= json.load(c)["params"]

local_server = True
app = Flask(__name__)
app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT='465',
    MAIL_USE_TLS=False,
    MAIL_USE_SSL = True,
   )
app.config['MAIL_USERNAME'] =params['gmail-user']
app.config['MAIL_PASSWORD']=params['gmail-pass']
mail= Mail(app)
if (local_server):
    app.config['SQLALCHEMY_DATABASE_URI'] = params['local_uri'] 
else:
     app.config['SQLALCHEMY_DATABASE_URI'] = params['prod_uri'] 
db = SQLAlchemy(app)


#config flask login


#database classes

class Contacts(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80),  nullable=False)
    email = db.Column(db.String(30),  nullable=False)
    phone_num = db.Column(db.String(12),  nullable=False)
    msg = db.Column(db.String(120),  nullable=False)
    date = db.Column(db.String(12),  nullable=True)


#register class

class Join(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80),  nullable=False)
    email_id = db.Column(db.String(30),  nullable=False)
    password = db.Column(db.String(80),  nullable=False)
    confirm = db.Column(db.String(80),  nullable=False)
    dob = db.Column(db.String(20),  nullable= False)
    gender = db.Column(db.String(120),  nullable=False)
    date = db.Column(db.String(12),  nullable=True)





#home
@app.route("/")
def home():
    return render_template('index.html',params=params)


#about us
@app.route("/about")
def about():
    return render_template('about_us.html',params=params)

#fitness tips
@app.route("/fitness")
def fitness():
    return render_template('fitness.html',params=params)

#contact us
@app.route("/contact", methods=['GET', 'POST'])
def contact():
    if(request.method == 'POST'):
        '''Add entry to database'''
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        msg = request.form.get('msg')

        entry = Contacts(name=name,email=email,phone_num=phone,msg=msg,date= datetime.now())
        db.session.add(entry)
        db.session.commit()
        mail.send_message('New massage from Fitness Club' + name,sender=email,recipients=[params['gmail-user']],body= msg + "\n"+ phone )
    return render_template('contact.html',params=params)

#registertion page
@app.route("/join",methods = ['GET','POST'])
def join():
    if(request.method == 'POST'):
        username = request.form.get('username')
        email_id =request.form.get('emailid')
        password= request.form.get('password')
        confirm= request.form.get('confirm')
        dob =request.form.get('dateOfb')
        gender =request.form.get('gender')
        #secure_password = sha256_crypt.encrypt(str(password))

        if password == confirm:
             entry1 = Join(username=username,email_id=email_id,password=password,confirm=confirm,dob=dob,gender=gender,date = datetime.now())
             db.session.add(entry1)
             db.session.commit()
             mail.send_message('New massage from Fitness Club' + username,sender=email_id,recipients=[params['gmail-user']],body=  username +"\n"+  email_id + "\n"+password+"\n"+dob + "\n"+ gender )
             flash("you are sucessfully registered and log in now","success")
             return redirect(url_for('login'))
        else:
            flash("password does not match","danger")
            return render_template("join.html",params=params)     
   
    return render_template('join.html',params=params)

#service
@app.route("/service")
def service():
    return render_template('service.html',params=params)


#log in
@app.route("/login",methods=['GET','POST'])
def login():
   
    return render_template('login.html',params=params)




if __name__ == '__main__':
    app.secret_key ="12345noorcooding"
    app.run(debug=True)