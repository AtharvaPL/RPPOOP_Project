from flask import Flask,render_template,request
from flask_mysqldb import MySQL


app=Flask(__name__)



app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']='DScl@123'
app.config['MYSQL_DB']='wscube'

mysql=MySQL(app)

@app.route('/',methods=['GET','POST'])

def book_return():
    if request.method=='POST':
        userdetails=request.form
        a=userdetails['bookname']
        b=userdetails['bookcode']
        c=userdetails['returnedby']
        d=userdetails['mis']
        e=userdetails['fine']
        f=userdetails['dateofreturn']
        cur=mysql.connection.cursor()
        cur.execute("INSERT INTO return_book(SrNo,BOOK_NAME,BOOK_CODE,RETURNED_BY,MIS,FINE,DATE_OF_RETURN) VALUES(NULL,%s,%s,%s,%s,%s,%s)",(a,b,c,d,e,f))
        mysql.connection.commit()
        cur.close()
        return 'success'


    return render_template('book_return.html')



if __name__=='__main__':
    app.run(debug=True)