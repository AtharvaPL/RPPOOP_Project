# from flask import Flask, render_template, request
# from flask_mysqldb import MySQL
# import MySQLdb.cursors
# app = Flask(__name__)

# #code for connection
# app.config['MYSQL_HOST'] = 'localhost'#hostname
# app.config['MYSQL_USER'] = 'root'#username
# app.config['MYSQL_PASSWORD'] = 'DScl@123'#password
# #in my case password is null so i am keeping empty
# app.config['MYSQL_DB'] = 'wscube'#database name

# mysql = MySQL(app)
# @app.route('/')

# @app.route('/issue',methods=['GET','POST'])
# def issue():
#     msg=''
#     #applying empty validation
#     if request.method == 'POST' and 'issuebook' in request.form and 'issueto' in request.form and 'issuedate' in request.form and 'bookdate' in request.form:
#         #passing HTML form data into python variable
#         n = request.form['issuebook']
#         t = request.form['issueto']
#         d = request.form['issuedate']
#         g = request.form['bookdate']
#         #creating variable for connection
#         cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
#         #query to check given data is present in database or no
#         cursor.execute('SELECT * FROM store_data WHERE PRO_NAME = % s', (n,))
#         #fetching data from MySQL
#         result = cursor.fetchone()
#         # if result:
#         #     msg = 'Project already exists !'
#         # else:
#             #executing query to insert new data into MySQL
#         cursor.execute('INSERT INTO store_data VALUES (NULL,% s, % s, % s,% s)', (n, t, d, g,))
#         mysql.connection.commit()
#             #displaying message
#         msg = 'You have successfully registered !'
#     elif request.method == 'POST':
#         msg = 'Please fill out the form !'
#     return render_template('issue.html', msg=msg)
# if __name__ == '__main__':
#     app.run(port=5000,debug=True)

from flask import Flask,render_template,request
from flask_mysqldb import MySQL
# import yaml
app=Flask(__name__)

# db=yaml.load(open('db.yaml'))

app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']='Atharva@28'
app.config['MYSQL_DB']='wscube'

mysql=MySQL(app)

@app.route('/',methods=['GET','POST'])
def index():
    if request.method=='POST':
        userdetails=request.form
        a=userdetails['issuebook']
        b=userdetails['issueto']
        c=userdetails['issuedate']
        d=userdetails['bookcode']
        cur=mysql.connection.cursor()
        cur.execute("INSERT INTO Issue_book_data(srNo,BOOK_TITLE,ISSUE_TO,DATE_OF_ISSUE,BOOK_CODE) VALUES(NULL,%s,%s,%s,%s)",(a,b,c,d))
        mysql.connection.commit()
        cur.close()
        return 'success'


    return render_template('index.html')



if __name__=='__main__':
    app.run(debug=True) 