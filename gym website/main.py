from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
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

class Contacts(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80),  nullable=False)
    email = db.Column(db.String(30),  nullable=False)
    phone_num = db.Column(db.String(12),  nullable=False)
    msg = db.Column(db.String(120),  nullable=False)
    date = db.Column(db.String(12),  nullable=True)


@app.route("/")
def home():
    return render_template('index.html',params=params)

@app.route("/about")
def about():
    return render_template('about_us.html',params=params)

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


@app.route("/join")
def join():
    return render_template('join.html',params=params)


@app.route("/service")
def service():
    return render_template('service.html',params=params)



if __name__ == '__main__':
    app.run(debug=True)