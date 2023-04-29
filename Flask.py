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


def AddBook(name,author,cupboardNo,quantity,isavailable,bookcode):
    Insert = "INSERT INTO data VALUES('{}','{}',{},{},{},{})".format(name,author,cupboardNo,quantity,isavailable,bookcode)
    Queries(connection,Insert)


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
    return render_template("add_a_book.html")

@app.route("/add_user")
def add_user():
    return render_template("add_user.html")

@app.route("/issue_book")
def issue():
    return render_template("issue_book.html")

@app.route("/page1")
def page1():
    return render_template("page1.html")

@app.route("/search_book")
def search_book():
    return render_template("search_book.html")

app.run(debug=True)
