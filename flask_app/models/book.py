from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import author

# model the class after the friend table from our database
class Book:
    def __init__( self , data ):
        self.id = data['id']
        self.title = data['title']
        self.num_of_pages = data['num_of_pages']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

        self.authors_favorited = []

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM books;"
        results = connectToMySQL('books_schema').query_db(query)
        books = []
        for book in results:
            books.append( cls(book) )
        return books
    
    @classmethod
    def save(cls, data ):
        query = """INSERT INTO books ( title, num_of_pages, created_at,updated_at ) 
        VALUES (%(title)s, %(num_of_pages)s, NOW() , NOW() );"""
        return connectToMySQL('books_schema').query_db( query, data )

    @classmethod
    def get_book_favorited_by_authors( cls , data ):
        query = """SELECT * FROM books 
        LEFT JOIN favorites ON favorites.book_id = books.id 
        LEFT JOIN authors ON favorites.author_id = authors.id WHERE books.id = %(id)s;"""
        results = connectToMySQL('books_schema').query_db( query , data )
        # results will be a list of topping objects with the burger attached to each row. 
        book = cls( results[0] )
        for row_from_db in results:
                # Now we parse the topping data to make instances of toppings and add them into our list.
            author_data = {
                "id" : row_from_db["authors.id"],
                "name" : row_from_db["name"],
                "created_at" : row_from_db["authors.created_at"],
                "updated_at" : row_from_db["authors.updated_at"]
            }
            book.authors_favorited.append(author.Author(author_data))
        return book

    @classmethod
    def savefavorite(cls, data ):
        query = """INSERT INTO favorites ( author_id, book_id ) 
        VALUES (%(author_id)s, %(book_id)s);"""
        return connectToMySQL('books_schema').query_db( query, data )