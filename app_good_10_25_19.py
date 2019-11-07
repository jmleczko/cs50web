from flask import Flask, flash, render_template, g, url_for, request, redirect
from flask_oidc import OpenIDConnect
from okta import UsersClient
from forms import BookSearchForm
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

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

search_by =''
@app.route('/search', methods=['GET', 'POST'])
@oidc.require_login
def dashboard():
    global search_by
    search_by = request.form['search_by']
    isbn = request.form['keyword']

    if request.form['search_by'] == "1":  # Author
        author = search_by
        db_session.execute("SELECT author FROM authors WHERE author = '%s'" % author,
                                  {"author": author}).fetchone()
        print("\nAuthor Found!\n\n"
             "Books by " + author + ":")

        print("   ISBN     | Year   |   Title")
        print("------------------------------")
        for row in db_session.execute(
                        "select isbn, title, year from books inner join authors on(books.author_id = authors.id) join years on(books.year_id = years.id) where author = '%s'" % author):
            print(str(row[0]) + '  |  ' + str(row[2]) + ' | ' + str(row[1]))

    elif request.form['search_by'] == "2":  # ISBN
        isbn = search_by
        db.execute("SELECT author FROM authors WHERE author = '%s'" % isbn,
                                  {"author": isbn}).fetchone()
        print("\nISBN Found!\n\n"
             "Books by " + isbn + ":")

        print("   ISBN     | Year   |   Title")
        print("------------------------------")
        for row in db.execute(
                        "select isbn, title, year from books inner join authors on(books.author_id = authors.id) join years on(books.year_id = years.id) where author = '%s'" % author):
            print(str(row[0]) + '  |  ' + str(row[2]) + ' | ' + str(row[1]))

    return render_template("search.html", form=search)


@app.route('/results')
def search_results(search):



    return render_template("results.html")







@app.route("/login")
@oidc.require_login
def login():
    return redirect(url_for(".dashboard"))


@app.route("/logout")
def logout():
    oidc.logout()
    return redirect(url_for(".index"))


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)



list_books_by_author()

