from flask import Flask,request,render_template,redirect
import requests
import os

class TestData(object):
    def __init__(self,type,title):
        self.type = type
        self.title = title
        
app = Flask(__name__)

@app.route("/",methods=["POST","GET"])
def index():

    if request.method == "POST":
        type = request.form["type"]
        title = request.form["title"]

        res = requests.post("http://backend:5000/test/add",data={"type":type,"title":title})

        if res.status_code == 200:
            return redirect("/test")

    return render_template("index.html")

@app.route("/test",methods=["GET"])
def data():

    res = requests.post("http://backend:5000/test/list").json()
    data = []

    for tdata in res["list"]:
        data.append(TestData(tdata[0],tdata[1]))

    return render_template("reviews.html",data=data)

app.run(host="0.0.0.0",port=5000)
