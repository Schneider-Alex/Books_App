from flask_app import app
from flask import render_template,redirect,request,session,flash
from flask_app.models import book
from flask_app.models import author



@app.route('/books')
def booksindex():
    return render_template("bookindex.html", all_books = book.Book.get_all())

@app.route('/create/authors')
def sendtoauthorpage():
    return redirect('/')

@app.route('/create_book', methods=["POST"])
def createbook():
    data = {
        'title' : request.form["title"],
        'num_of_pages' : request.form['pages']
    }
    book.Book.save(data)
    return  redirect('/books')

@app.route('/bookfavauthors/<int:bookid>')
def bookfavorites(bookid):
    data = {
        "id" : bookid
    }
    return render_template("booksfavorite.html", specificbook=book.Book.get_book_favorited_by_authors(data ),all_authors=author.Author.get_all()) 

@app.route('/savefavoritefrombook/<bookid>',methods=["POST"])
def savefavorite(bookid):
    data ={
        'author_id' : request.form["author_id"],
        'book_id' : bookid
    }
    book.Book.savefavorite(data)

    return redirect(f'/bookfavauthors/{bookid}')

