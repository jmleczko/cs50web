from flask import Flask, flash, render_template, g, url_for, request, redirect
from flask_oidc import OpenIDConnect
from okta import UsersClient
from forms import BookSearchForm
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

##### Master Branch Copy #####

engine = create_engine(
    "postgres://ynsnlwrsihabfl:4f4b80293dacce103e5d5956512cb4f7b0fbf91e3fe9a3d731329c9fe4f9a22a@ec2-54-221-201-212.compute-1.amazonaws.com:5432/dfha9vsh7kdrei",
    convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

engine = create_engine(
    'postgres://ynsnlwrsihabfl:4f4b80293dacce103e5d5956512cb4f7b0fbf91e3fe9a3d731329c9fe4f9a22a@ec2-54-221-201-212.compute-1.amazonaws.com:5432/dfha9vsh7kdrei')

Base = declarative_base()

Session = sessionmaker(bind=engine)
Session.configure(bind=engine)
session = Session()

app = Flask(__name__)
app.config["OIDC_CLIENT_SECRETS"] = "client_secrets.json"
app.config["OIDC_COOKIE_SECURE"] = False
app.config["OIDC_CALLBACK_ROUTE"] = "/oidc/callback"
app.config["OIDC_SCOPES"] = ["openid", "email", "profile"]
app.config["SECRET_KEY"] = "{{ LONG_RANDOM_STRING }}"
app.config["OIDC_ID_TOKEN_COOKIE_NAME"] = "oidc_token"
oidc = OpenIDConnect(app)
token = "00zZebnIbNUilkHujTN23qdbzQTUivu9xU2KoA9fPM"
okta_client = UsersClient("https://dev-323916.okta.com", token)



@app.before_request
def before_request():
    if oidc.user_loggedin:
        g.user = okta_client.get_user(oidc.user_getfield("sub"))
    else:
        g.user = None


@app.route("/")
def index():
    return render_template("index.html")


@app.route('/search', methods=['GET', 'POST'])
@oidc.require_login
def search():
    return render_template('search.html',data=[{'name':'Author Name'}, {'name':'ISBN'}])


@app.route("/submit" , methods=['GET', 'POST'])
def submit():
    select = str(request.form.get('comp_select'))
    keyword = str(request.form.get('keyword'))

    if select == "Author Name":
        choice = "You chose " + select + keyword
        return choice
    else:
        choice = "You chose " + select + keyword
        return choice

    ## Need to figure out how to query the db for the author name based on user input. should be
    ## case insensitive and need to do a if part of name in db, then take the whole authors name and
    ## to variable author. Then execute the print statement that pulls all books by that author
    ## app_good_10_25.py has the correct examples of the print statement 888-800-5234


@app.route("/login")
@oidc.require_login
def login():
    return redirect(url_for("search"))
    # return redirect(url_for(".dashboard"))



@app.route("/logout")
def logout():
    oidc.logout()
    return redirect(url_for(".index"))


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)

