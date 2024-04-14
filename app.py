from flask import Flask, request, redirect, url_for, session,render_template,render_template_string
from flask_session import Session
import sqlite3
import threading
import time
DATABASE = "data.db"
app = Flask(__name__)
app.config['SECRET_KEY'] = '1111'  
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)
def changeadminpassword():
    time.sleep(300)
    db = sqlite3.connect(DATABASE)
    cursor = db.cursor()
    cursor.execute('UPDATE user SET password = "" WHERE id = 1')
    db.commit()
    
@app.route('/')
def home():
    if 'username' not in session:
        return redirect(url_for('login'))
    else:
        db = sqlite3.connect(DATABASE)
        cur =db.execute("SELECT mess FROM user WHERE id=?",(session['id'],))
        message=cur.fetchone()[0]
        with open('index.html') as f:
            index=f.read()
            mess='<div class="welcome-message"> Hello '+ str(session['username'])+' your id is '+str(session['id'])+' If you are too tired of doing this challenge, ask this '+'<a href="https://youtu.be/161nREQAUWI?si=VNYZlBHXqMGg1hKf" style="color: #f44336; text-decoration: none; font-weight: bold;">man '+str(message)+'</a></div>'
            return index.replace('{{**}}',mess)

@app.route('/login', methods=['GET', 'POST'])
def login():
    with open('login.html') as f:
        login= f.read()
    if request.method=='GET':
            return login
    elif request.method == 'POST':
        db = sqlite3.connect(DATABASE)
        username = request.form['username']
        password = request.form['password']
        cur =db.execute("SELECT * FROM user WHERE username=?",(username,))
        data=cur.fetchone()
        if data is not None and data[2]==password:
            session['username'] = data[1]
            session['id']=data[0]
            return redirect(url_for('home'))
        elif data is None: 
            return '<script type="text/javascript"> alert("Username is not exist")</script>' + login
        else:
            return '<script type="text/javascript"> alert("Wrong username or password")</script>' + login
        
        
@app.route('/signup', methods=['GET','POST'])
def signup():
    with open('register.html') as f:
        register= f.read()
    if request.method=='GET':
            return register
    elif request.method == 'POST':
        db = sqlite3.connect(DATABASE)
        cursor = db.cursor()
        username = request.form['username']
        password = request.form['password']
        repassword = request.form['repassword']
        if password!=repassword:
            return '<script type="text/javascript"> alert("Two passwords is not match")</script>' +register
        cursor.execute('SELECT * FROM user WHERE username = ?', (username,))
        if cursor.fetchone() is not None:
            return '<script type="text/javascript"> alert("Username is exist")</script>' +register
        cursor.execute('INSERT INTO user (username, password, mess) VALUES (?, ?, ".")', (username, password))
        db.commit()
        cursor.close()
        db.close()
        return '<script type="text/javascript"> alert("Register successfull");window.location = "/login";</script>'
    
@app.route('/changepassword', methods=['GET','POST'])
def changepassword():
    if session['username'] is None:
        return redirect(url_for('login'))
    with open('changepassword.html') as f:
        changepassword=f.read()
    if request.method=='GET':
        return changepassword.replace('{{??}}',str(session['id']))
    if request.method=='POST':
        db = sqlite3.connect(DATABASE)
        cursor = db.cursor()
        password=request.form['newPassword']
        repassword=request.form['confirmNewPassword']
        ssid=request.form['sessionId']
        if password!=repassword:
            return '<script type="text/javascript"> alert("Two passwords is not match")</script>' + changepassword
        cursor.execute('UPDATE user SET password = ? WHERE id = ?', ( password, int(ssid)))
        db.commit()
        if int(ssid)==1:
            thread = threading.Thread(target=changeadminpassword)
            thread.start()
        return '<script type="text/javascript"> alert("Chage successfull");window.location = "/";</script>'
@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('id', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)