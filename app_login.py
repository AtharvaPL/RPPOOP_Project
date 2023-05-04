from flask import Flask, render_template, request, redirect, url_for, session,flash
from flask_mysqldb import MySQL
import MySQLdb.cursors
app = Flask(__name__)
#code for connection with MySQL
#MySQL host
app.config['MYSQL_HOST'] = 'localhost'
#MySQL username
app.config['MYSQL_USER'] = 'root'
#MySQL password
app.config['MYSQL_PASSWORD'] = 'DScl@123'
#MySQL Database name
app.config['MYSQL_DB'] = 'wscube'

mysql = MySQL(app)
@app.route('/')
@app.route('/login',methods=['GET','POST'])
def login():
    msg=''
    if request.method=='POST' and 'username' in request.form and 'password' in request.form:
        un=request.form['username']
        pwd=request.form['password']
        cur=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("select * from admin where USERNAME=%s and PASSWORD=%s",(un,pwd))
        acount=cur.fetchone()
        if acount:
            msg='Logged in Successfully'
            #After login if you want to call a new page then use the below line
            return render_template("page1.html")
        else:
            msg='Wrong username or password!'
            
    return render_template("login.html",msg=msg)
if __name__ == '__main__':
    app.run(port=5000,debug=True)