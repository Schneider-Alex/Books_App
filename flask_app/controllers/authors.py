from flask_app import app
from flask import render_template,redirect,request,session,flash
from flask_app.models import author, book



@app.route('/')
def authorsindex():
    return render_template("authorindex.html", all_authors = author.Author.get_all())

@app.route('/create/book')
def sendtobookpage():
    return redirect('/books')

@app.route('/create_author', methods=["POST"])
def createauthor():
    data = {
        'name' : request.form["name"]
    }
    author.Author.save(data)
    return  redirect('/')

@app.route('/authorsfavbooks/<authorid>')
def authorfavoriters(authorid):
    data = {
        "id" : authorid
    }
    return render_template("authorsfavorite.html", specificauthor=author.Author.get_authors_favorite_books(data),all_books=book.Book.get_all()) 

@app.route('/savefavoritefromauthor/<authorid>',methods=["POST"])
def savefavorite2(authorid):
    data ={
        'author_id' : authorid,
        'book_id' : request.form["book_id"]
    }
    book.Book.savefavorite(data)

    return redirect(f'/authorsfavbooks/{authorid}')
