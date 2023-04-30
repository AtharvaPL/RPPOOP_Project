from flask import Flask,render_template,request,session
import mysql.connector
from mysql.connector import Error
import pandas as pd

app = Flask(__name__)

def connect_mysql(hostname,username,password):
    connection = None
    try:
        connection = mysql.connector.connect(host = hostname,user = username,passwd = password)
        print("MySQL connection successful!")
    except Error as err:
        print(f"Error:'{err}'" )
    return connection
connection=connect_mysql("localhost","root","Atharva@28")

def Database_Connection(hostname,username,password,db,connection):
    DatabaseConnection = None
    try:
        DatabaseConnection = mysql.connector.connect(host = hostname, user = username, passwd = password,database = db)
        print("Database Connected successfully")
    except Error as err:
        print(f"Error: '{err}'")
    return DatabaseConnection
DatabaseConnection = Database_Connection("localhost","root","Atharva@28","Books",connection)


def Queries(connection,query):
    cursor = connection.cursor(buffered=True)
    try:
        cursor.execute(query)
        connection.commit()
        print("Query was successful")
    except Error as err:
        print(f"Error: '{err}'")
Use_Database = "USE books;"
Queries(connection,Use_Database)

def find_byName(name):
    IsAvailable = "SELECT * FROM data WHERE (name='{}')".format(name)
    result = read(connection,IsAvailable)
    return result

def find_byBookCode(bookcode):
    IsAvailable = "SELECT * FROM data WHERE (bookcode={})".format(bookcode)
    result = read(connection,IsAvailable)
    return result


def IssueBook_byName(name):
    result = find_byName(name)
    if(result[0][-2]):
        if(result[0][3]==1):
            Update = """UPDATE DATA
            SET isavailable=0
            WHERE Name='{}';""".format(name)
            Queries(connection,Update)
        Update = """UPDATE data
        SET quantity = {}
        WHERE Name='{}';""".format(result[0][3]-1,name)
        Queries(connection,Update)
    else:
        print("Book not available")

def IssueBook_byBookCode(bookcode):
    result = find_byBookCode(bookcode)
    if(result[0][-2]):
        if(result[0][3]==1):
            Update = """UPDATE DATA
            SET isavailable=0
            WHERE bookcode={};""".format(bookcode)
            Queries(connection,Update)
        Update = """UPDATE data
        SET quantity = {}
        WHERE bookcode={};""".format(result[0][3]-1,bookcode)
        Queries(connection,Update)
    else:
        print("Book not available")

def AddBook(name,author,cupboardNo,quantity,isavailable,bookcode):
    Insert = "INSERT INTO data VALUES('{}','{}',{},{},{},{})".format(name,author,cupboardNo,quantity,isavailable,bookcode)
    Queries(connection,Insert)

def returnbook_byName(name):
    result = find_byName(name)
    if(result[0][3]==0):
        Update = """UPDATE DATA
        SET isavailable=1
        WHERE name='{}';""".format(name)
        Queries(connection,Update)
    Update = """UPDATE data
    SET quantity = {}
    WHERE name='{}';""".format(result[0][3]+1,name)
    Queries(connection,Update)   

def returnbook_byBookCode(bookcode):
    result = find_byBookCode(bookcode)
    if(result[0][3]==0):
        Update = """UPDATE DATA
        SET isavailable=1
        WHERE bookcode={};""".format(bookcode)
        Queries(connection,Update)
    Update = """UPDATE data
    SET quantity = {}
    WHERE bookcode={};""".format(result[0][3]+1,bookcode)
    Queries(connection,Update)

def read(connection,query):
    cursor = connection.cursor(buffered=True)
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except:
        pass 



@app.route("/login",methods=["GET", "POST"])
def login():
        return render_template("login.html")




@app.route("/add_a_book",methods=["GET", "POST"])
def add_a_book():
    if request.method=="POST": # type: ignore
        name = request.form.get("name") # type: ignore
        author = request.form.get("author") # type: ignore
        cupboardNo = request.form.get("cupboardNo") # type: ignore
        quantity = request.form.get("quantity") # type: ignore
        bookcode = request.form.get("bookcode") # type: ignore
        AddBook(name,author,cupboardNo,quantity,1,bookcode)
    return render_template("add_a_book.html")

# def add_book():
    # name = request.form.get("name") # type: ignore
    # print(name)


@app.route("/add_user",methods=["GET", "POST"])
def add_user():
    return render_template("add_user.html")

@app.route("/issue_book",methods=["GET", "POST"])
def issue():
    if request.method == "POST": # type: ignore
        title = request.form.get("title") # type: ignore
        IssueBook_byName(title)
    return render_template("issue_book.html")

@app.route("/page1",methods=["GET", "POST"])
def page1():
    return render_template("page1.html")

@app.route("/search_book",methods=["GET", "POST"])
def search_book():
    if request.method=="POST": # type: ignore
        name=request.form.get("name") # type: ignore
        Select = """SELECT * FROM data
        Where name LIKE '%{}%'""".format(name)
        Queries(connection,Select)
        info=read(connection,Select)
        df = pd.DataFrame()
        for i in info:
            df1 = pd.DataFrame(list(i)).T
            df = pd.concat([df,df1])
        df.to_html('templates/search_book.html')
        return render_template("search_book.html",info=df)
    else:
        return render_template("search_book.html")

app.run(debug=True)