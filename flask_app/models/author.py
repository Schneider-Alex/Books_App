from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import book

# model the class after the friend table from our database
class Author:
    def __init__( self , data ):
        self.id = data['id']
        self.name = data['name']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

        self.books = []
    
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM authors;"
        # make sure to call the connectToMySQL function with the schema you are targeting.
        results = connectToMySQL('books_schema').query_db(query)
        # Create an empty list to append our instances of friends
        authors = []
        # Iterate over the db results and create instances of friends with cls.
        for author in results:
            authors.append( cls(author)) 
        return authors
    
    @classmethod
    def save(cls, data ):
        query = """INSERT INTO authors ( name, created_at,updated_at ) 
        VALUES (%(name)s, NOW() , NOW() );"""
        # data is a dictionary that will be passed into the save method from server.py
        return connectToMySQL('books_schema').query_db( query, data )

    @classmethod
    def get_authors_favorite_books( cls , data ):
        query = """SELECT * FROM authors 
        LEFT JOIN favorites ON favorites.author_id = authors.id 
        LEFT JOIN books ON favorites.book_id = books.id WHERE authors.id = %(id)s;"""
        results = connectToMySQL('books_schema').query_db( query , data )
        print(results)
        author = cls( results[0] )
        for row_from_db in results:
                # Now we parse the topping data to make instances of toppings and add them into our lit.
            book_data = {
                "id" : row_from_db["books.id"],
                "title" : row_from_db["title"],
                "num_of_pages" : row_from_db['num_of_pages'],
                "created_at" : row_from_db["books.created_at"],
                "updated_at" : row_from_db["books.updated_at"]
            }
            author.books.append(book.Book(book_data))
        return author