from flask import Flask,render_template,request
from flask_mysqldb import MySQL

app=Flask(__name__)



app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']='DScl@123'
app.config['MYSQL_DB']='wscube'

mysql=MySQL(app)

@app.route('/',methods=['GET','POST'])

def issue_book():
    if request.method=='POST':
        userdetails=request.form
        a=userdetails['issuebook']
        b=userdetails['issueto']
        c=userdetails['issuedate']
        d=userdetails['bookcode']
        cur=mysql.connection.cursor()
        cur.execute("INSERT INTO issue_book_data(srNo,BOOK_TITLE,ISSUE_TO,DATE_OF_ISSUE,BOOK_CODE) VALUES(NULL,%s,%s,%s,%s)",(a,b,c,d))
        mysql.connection.commit()
        cur.close()
        return 'success'


    return render_template('issue_book.html')



if __name__=='__main__':
    app.run(debug=True)