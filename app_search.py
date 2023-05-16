from flask import Flask,render_template,request
from flask_mysqldb import MySQL


app=Flask(__name__)



app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']='DScl@123'
app.config['MYSQL_DB']='wscube'

mysql=MySQL(app)

@app.route('/',methods=['GET','POST'])

def search_page():
    return render_template("search_book.html")

@app.route("/search_book", methods=["POST"])
def search():
    if request.method=='POST':
            query = request.form["query"]
            cursor = mysql.connection.cursor()
            cursor.execute("SELECT * FROM issue_book_data WHERE BOOK_TITLE LIKE %s", (f"%{query}%",))
            results = cursor.fetchall()
            return render_template("search_book.html", results=results)
    
    
          
         



       

if __name__ == "__main__":
    app.run(debug=True)