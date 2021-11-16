from flask import Flask,request,render_template,redirect
import psycopg2
import os
import time

DB_USER = os.environ["DB_USER"]
DB_PASSWORD = os.environ["DB_PASS"]
DB = os.environ["DB"]
DB_HOST = os.environ["DB_HOST"]

app = Flask(__name__)

def init_tables():

    CREATE_TABLE = "CREATE TABLE IF NOT EXISTS TESTDATA (id TEXT NOT NULL, type TEXT NOT NULL,title TEXT NOT NULL)"
    conn = psycopg2.connect(host=DB_HOST,database=DB, user=DB_USER, password=DB_PASSWORD)
    cursor = conn.cursor()
    cursor.execute(CREATE_TABLE)
    conn.commit()
    cursor.close()
    conn.close()

def add_data(type,title):

    ADD_DATA = "INSERT INTO TESTDATA (type,title) VALUES (%s,%s)"
    conn = psycopg2.connect(host=DB_HOST,database=DB, user=DB_USER, password=DB_PASSWORD)
    cursor = conn.cursor()
    cursor.execute(ADD_DATA,(type,title))
    conn.commit()
    cursor.close()
    conn.close()

def load_data():

    data = []

    LOAD_DATA = "SELECT * from TESTDATA"
    conn = psycopg2.connect(host=DB_HOST,database=DB, user=DB_USER, password=DB_PASSWORD)
    cursor = conn.cursor()
    cursor.execute(LOAD_DATA)
    results = cursor.fetchall()

    for row in results:
        data.append((row[0],row[1],row[2]))
    cursor.close()
    conn.close()

    return data

@app.route("/test/add",methods=["POST"])
def adddata():

    
    type = request.form["type"]
    title = request.form["title"]

    add_data(type,title)

    return {"success":True}

@app.route("/test/list",methods=["POST"])
def listdata():

    data = load_data()

    return {"success":True,"list":data}

app.run(host="0.0.0.0",port=5000)
