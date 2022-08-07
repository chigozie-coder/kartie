import os
from flask import Flask, render_template, request, url_for, redirect, session, jsonify
from tinydb import *
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from flask_cors import CORS
basedir = os.path.abspath(os.path.dirname(__file__))
from tinydb import TinyDB, Query
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =\
        'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = ""
db = SQLAlchemy(app)
tdb=TinyDB("database.txt")
qdb=Query()
CORS(app)
class Products(db.Model):
  pname=db.Column(db.String, nullable=False)
  id=db.Column(db.Integer, primary_key=True, nullable=False)
  des=db.Column(db.String, nullable=False)
  price=db.Column(db.String, nullable=False)
  img=db.Column(db.String, nullable=False)
  cat=db.Column(db.String, nullable=False)
  def __repr__(self):
    """docstring for fname"""
    return f'<Product {self.pname}>'
@app.route('/')
def index():
    shoes=Products.query.filter_by(cat="shoes").all()
    
    gadgets=Products.query.filter_by(cat="gadgets").all()
    
    clothes=Products.query.filter_by(cat="clothes").all()
    return render_template("index.html", shoes=shoes, gadgets=gadgets, clothes=clothes, Getuser=Getuser)
@app.route('/category/<cat>')
def cat(cat):
    kat=cat
    pd=Products.query.filter_by(cat=cat).all()
    return render_template("category.html",pd=pd, cat=kat)
@app.route("/login", methods=["POST", "GET"])
def login():
  # if form is submited
    if request.method == "POST":
        # record the user name
        email=request.form.get("email")
        password=request.form.get("pass")
        quer=tdb.search(qdb.email==email)
        if quer:
            if quer[0]["pass"]==password:
                session["email"]=email
                return redirect(url_for('index'))
            else:
                return render_template("login.html", mess="Incorrect pass")
        else:
            return render_template("login.html", mess="Not signed up")
    return render_template("login.html")
@app.route('/signup', methods=["GET", "POST"])
def signup():
    if request.method=="POST":
        email=request.form["email"]
        password=request.form["pass"]
        name=request.form["name"]
        quer=tdb.search(qdb.email==email)
        if not len(quer)==0:
            return redirect(url_for('login'))
        else:
            tdb.insert({"email":email, "pass": password, "name": name, "cart":[]})
            return redirect(url_for('login'))
    return render_template("signup.html")
@app.route('/create')
def createacct():
    return render_template("signup.html")
@app.route('/cart')
def cart():
    if not session.get("email"):
        # if not there in the session then redirect to the login page
        return redirect("/login")
    else:
        user=tdb.search(qdb.email==session["email"])
        items= user[0]["cart"]
        return render_template("cart.html", items=items, Getcarddata=Getcarddata)
    return render_template("cart.html")
@app.route('/logout')
def logout():
    session["email"]=None
    return redirect('/')
@app.route('/search', methods=["GET", "POST"])
def search():
    if request.method=="POST":
        q=request.form["q"]
        spd=Products.query.filter_by(pname=q).all()
        if spd:
            return render_template("search.html", pd=spd, q=q)
        else:
            return render_template("search.html", mess="No results found",q=q)
    return render_template("search.html")
@app.route('/api/<id>', methods=["GET"])
def api(id):
    apn=Getcarddata(id).pname()
    ades=Getcarddata(id).des()
    aimg=Getcarddata(id).img()
    aprice=Getcarddata(id).price()
    acat=Getcarddata(id).cat()
    return jsonify({"pname":apn,"des":ades,"img":aimg,"price":aprice,"category":acat})
@app.route('/addtocart/<id>')
def addtocart(id):
    if not session.get("email"):
        # if not there in the session then redirect to the login page
        return redirect("/login")
    else:
        user=tdb.search(qdb.email==session["email"])
        items= user[0]["cart"]
        name=user[0]["name"]
        email=user[0]["email"]
        password=user[0]["pass"]
        items.append(str(id))
        tdb.update({"email":email, "pass": password, "name": name, "cart":items})
        return redirect('/cart')
    return redirect("/cart")
@app.route('/rfromcart/<id>')
def rfromcart(id):
    if not session.get("email"):
        # if not there in the session then redirect to the login page
        return redirect("/login")
    else:
        user=tdb.search(qdb.email==session["email"])
        items= user[0]["cart"]
        name=user[0]["name"]
        email=user[0]["email"]
        password=user[0]["pass"]
        items.remove(str(id))
        tdb.update({"email":email, "pass": password, "name": name, "cart":items})
        return redirect('/cart')
    return redirect("/cart")
class Getcarddata:
    def __init__(self, id):
        self.id=id
        self.pd=Products.query.filter_by(id=self.id).first()
    def pname(self):
        return self.pd.pname
    def des(self):
        return self.pd.des
    def img(self):
        return self.pd.img
    def cat(self):
        return self.pd.cat
    def price(self):
        return self.pd.price
class Getuser:
    def __init__(self, email):
        self.email=email
        self.user=tdb.search(qdb.email==session["email"])
    def name(self):
        return self.user[0]["name"]

@app.errorhandler(404)
def page_not_found(e):
   return render_template('404.html'),404
if __name__=="__main__":
    app.run(debug=True)

