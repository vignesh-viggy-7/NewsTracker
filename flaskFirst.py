from collections import UserDict
import ibm_db
from flask import Flask,render_template,request,redirect,url_for,session
import re
app=Flask(__name__)

app.secret_key='a'
@app.route('/')
def hello():
    return "local server running"

    #webpages User Interface 

@app.route('/home')
def homePage():
    return render_template("NewsTracker.html")


@app.route('/registration',methods=['GET','POST'])
def registraion():
    msg=''
    if request.method=='POST':
        username=request.form['username']
        email=request.form['email']
        password=request.form['password']
        confirmPassword=request.form['confirmPassword']
        sql="SELECT * FROM users WHERE username=?"
        stmt=ibm_db.prepare(conn,sql)
        ibm_db.bind_param(stmt,1,username)
        ibm_db.execute(stmt)
        account=ibm_db.fetch_assoc(stmt)
        print(account)
        if account:
            msg="Account already exist!"
        elif not re.match(r'[^@]+@[^@]+\.[^@]+',email):
            msg="Invalid email address :("
        elif not re.match(r'[A-za-z0-9]+',username):
            msg='Name must have only Alphabets and numbers '
        elif not re.match(password,confirmPassword):
            msg='please check password and confirm'
        else:
            insert_sql="INSERT INTO users VALUES (?,?,?,?)"
            prep_stmt=ibm_db.prepare(conn,insert_sql)
            ibm_db.bind_param(prep_stmt,1,username)
            ibm_db.bind_param(prep_stmt,2,email)
            ibm_db.bind_param(prep_stmt,3,password)
            ibm_db.bind_param(prep_stmt,4,confirmPassword)
            ibm_db.execute(prep_stmt)
            msg="You have SUCCESSFULLY REGISTERED"
    elif request.method=="POST":
            msg='PLEASE FILL THE FORM'
    return render_template("NewsTrackerRegister.html",msg=msg)


@app.route('/login',methods=['GET','POST']) 
def loginPage():
    
    global userid
    msg=''
    
    if request.method=='POST':
        username=request.form['username']
        password=request.form['password']
        sql="SELECT * FROM users where username=? AND password=?"
        stmt=ibm_db.prepare(conn,sql)
        ibm_db.bind_param(stmt,1,username)
        ibm_db.bind_param(stmt,2,password)
        ibm_db.execute(stmt)
        account=ibm_db.fetch_assoc(stmt)
        print(account)
        if account:
            session['loggedin']=True
            session['id']=account['USERNAME']
            userid=account['USERNAME']
            session['username']=account['USERNAME']
            msg='logged in successfully !'
            return render_template("NewsTracker.html",msg=msg)
        else:
            msg='Incorrect username or password !'
    return render_template("CADform.html",msg=msg)


@app.route('/cool')
def bootstrap():
   return render_template("bootstrapdemo.html")


#Database connection code IBM DB2

conn=ibm_db.connect("HOSTNAME=125f9f61-9715-46f9-9399-c8177b21803b.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud;DATABASE=bludb;PORT=30426;SECURITY=SSL;SSLServerCertification=dbCertificate.crt; UID=dcc80627;PWD=9SLbAkYtWXrZUDT7",'','')


if __name__==('__main__'):
    
    app.run(debug=True)
