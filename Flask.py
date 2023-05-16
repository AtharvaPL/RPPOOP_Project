from flask import Flask, render_template, request, redirect, url_for, session,flash
from flask_mysqldb import MySQL
import MySQLdb.cursors
import mysql.connector
from mysql.connector import Error
import pandas as pd
from datetime import date

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


# def IssueBook_byName(name,mis):
#     result = find_byName(name)
#     if(result[0][-2]):
#         if(result[0][3]==1):
#             Update = """UPDATE DATA
#             SET isavailable=0
#             WHERE Name='{}';""".format(name)
#             Queries(connection,Update)
#         Update = """UPDATE data
#         SET quantity = {}
#         WHERE Name='{}';""".format(result[0][3]-1,name)
#         Queries(connection,Update)

#             # User_Query = """INSERT INTO user VALUES('{}',{},)"""
#     else:
#         print("Book not available")



def IssueBook_byBookCode(bookcode,mis):
    # userdb = get_user_db(mis)
    find = "SELECT * FROM user WHERE mis={}".format(mis)
    userdb = read(connection,find)
    if(userdb):
        if(userdb[0][2] and userdb[0][4] and userdb[0][6]):
            print("You cannot issue more books, please first return books")
        else:
            if((userdb[0][3]!=None and (userdb[0][3]-date.today()).days<-30) or (userdb[0][5]!=None and (userdb[0][5]-date.today()).days<-30) or (userdb[0][7]!=None and (userdb[0][7]-date.today()).days<-30)):
                fine = 0
                if(userdb[0][3] and (userdb[0][3]-date.today()).days<-30):
                    fine = fine + ((date.today()-userdb[0][3]).days-30)*100
                if(userdb[0][5] and (userdb[0][5]-date.today()).days<-30):
                    fine = fine + ((date.today()-userdb[0][5]).days-30)*100
                if(userdb[0][7] and (userdb[0][7]-date.today()).days<-30):
                    fine = fine + ((date.today()-userdb[0][7]).days-30)*100
                print("You have exceeded your return deadline, please first return books and your fine is {}".format(fine))
            else:
                if((userdb[0][2]!=None and userdb[0][2]==bookcode) or (userdb[0][4]!=None and userdb[0][4]==bookcode) or (userdb[0][6]!=None and userdb[0][6]==bookcode)):
                    print("You have already issued this book, cannot reissue the same book again")
                else:
                    bookdb = find_byBookCode(bookcode)
                    if(bookdb[0][-2]):
                        if(bookdb[0][3]==1):
                            Update = """UPDATE DATA
                            SET isavailable=0
                            WHERE bookcode={};""".format(bookcode)
                            Queries(connection,Update)
                        Update = """UPDATE data
                        SET quantity = {}
                        WHERE bookcode={};""".format(bookdb[0][3]-1,bookcode)
                        Queries(connection,Update)
                        if(userdb[0][2]==None):
                            Update = """UPDATE user
                            SET Book1 = {},
                            Issue1 = '{}'
                            WHERE MIS = {};""".format(bookcode,date.today(),mis)
                            print(date.today())
                        elif(userdb[0][4]==None):
                            Update = """UPDATE user
                            SET Book2 = {},
                            Issue2 = '{}'
                            WHERE MIS = {};""".format(bookcode,date.today(),mis)
                        else:
                            Update = """UPDATE user
                            SET Book3 = {},
                            Issue3 = '{}'
                            WHERE MIS = {};""".format(bookcode,date.today(),mis)
                        Queries(connection,Update)
                    else:
                        print("Book not available")
    else:
        print("User not found, please register first")


def AddBook(name,author,cupboardNo,quantity,isavailable,bookcode):
    Insert = "INSERT INTO data VALUES('{}','{}',{},{},{},{})".format(name,author,cupboardNo,quantity,isavailable,bookcode)
    Queries(connection,Insert)

# def returnbook_byName(name):
#     result = find_byName(name)
#     if(result[0][-2]==0):
#         Update = """UPDATE DATA
#         SET isavailable=1
#         WHERE name='{}';""".format(name)
#         Queries(connection,Update)
#     Update = """UPDATE data
#     SET quantity = {}
#     WHERE name='{}';""".format(result[0][3]+1,name)
#     Queries(connection,Update)   

def returnbook_byBookCode(bookcode,mis):
    find = "SELECT * FROM user WHERE mis={}".format(mis)
    userdb = read(connection,find)
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
    fine=0
    if(userdb[0][2] and userdb[0][2]==bookcode):
        if((userdb[0][3]-date.today()).days<-30):
            fine = fine + ((date.today()-userdb[0][3]).days-30)*100
        Update="""Update user
        SET Book1=NULL,
        Issue1=NULL
        WHERE MIS={};""".format(mis)
    elif(userdb[0][4] and userdb[0][4]==bookcode):
        if((userdb[0][5]-date.today()).days<-30):
            fine = fine + ((date.today()-userdb[0][5]).days-30)*100
        Update="""Update user
        SET Book2=NULL,
        Issue2=NULL
        WHERE MIS={};""".format(mis)
    else:
        if((userdb[0][7]-date.today()).days<-30):
            fine = fine + ((date.today()-userdb[0][7]).days-30)*100
        Update="""Update user
        SET Book3=NULL,
        Issue3=NULL
        WHERE MIS={};""".format(mis)
    if(fine):
        print("Please pay a fine of {}".format(fine))
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

def add_user_func(connection,name,mis):
    Query = """INSERT INTO user VALUES('{}',{},NULL,NULL,NULL,NULL,NULL,NULL)""".format(name,mis)
    Queries(connection,Query)


# @app.route("/login",methods=["GET", "POST"])
# def login():
#         return render_template("login.html")

@app.route('/login',methods=['GET','POST'])
def login():
    msg=''
    if request.method=='POST' and 'username' in request.form and 'password' in request.form:
        UID=request.form['username']
        pwd=request.form['password']
        cur=connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("select * from login where UserId=%s and Password=%s",(UID,pwd))
        account=cur.fetchone()
        if account:
            msg='Logged in Successfully'
            #After login if you want to call a new page then use the below line
            return render_template("page1.html")
        else:
            msg='Wrong username or password!'
            
    return render_template("login.html",msg=msg)


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
    if request.method == "POST":
        name = request.form.get("name") # type: ignore
        mis = request.form.get("mis") # type: ignore
        add_user_func(connection,name,mis)
    return render_template("add_user.html")

@app.route("/issue_book",methods=["GET", "POST"])
def issue():
    if request.method == "POST": # type: ignore
        # title = request.form.get("title") # type: ignore
        # MIS = request.form.get("MIS") # type: ignore
        # IssueBook_byName(title,MIS)
        bookcode = request.form.get("bookcode") # type: ignore
        mis = request.form.get("MIS") # type: ignore
        IssueBook_byBookCode(bookcode,mis)
    return render_template("issue_book.html")

@app.route("/book_return",methods=["GET", "POST"])
def return_book():
    if request.method=='POST':
        bookcode = request.form.get("bookcode") # type: ignore
        # mis = request.form.get("MIS") # type: ignore
        mis=112103079
        returnbook_byBookCode(bookcode,mis)
    return render_template('book_return.html')

@app.route("/page1",methods=["GET", "POST"])
def page1():
    return render_template("page1.html")

@app.route("/search_book",methods=["GET", "POST"])
def search_book():
    if request.method=="POST": # type: ignore
        case = request.form.get("for_search")
        query=request.form.get("query") # type: ignore
        if(case=="title"):
            Select = """SELECT * FROM data
            Where name LIKE '%{}%'""".format(query)
        else:
            Select = """SELECT * FROM data
            Where author LIKE '%{}%'""".format(query)
        cursor = connection.cursor()
        cursor.execute(Select)
        results = cursor.fetchall()
        return render_template("search_book.html", results=results)
    else:
        return render_template("search_book.html")


app.run(debug=True)