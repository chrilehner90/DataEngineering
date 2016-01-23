import config
import sys
import MySQLdb
import os


def setup_database(connection, cursor):
    cursor.execute("DROP TABLE IF EXISTS books")
    cursor.execute("CREATE TABLE books(id INT PRIMARY KEY AUTO_INCREMENT, book MEDIUMTEXT NOT NULL)")

    cursor.execute("DROP TABLE IF EXISTS books_fulltext_index")
    cursor.execute("CREATE TABLE books_fulltext_index(id INT PRIMARY KEY AUTO_INCREMENT, book MEDIUMTEXT NOT NULL)")

    connection.commit()


def write_books(connection, cursor):
    for file_name in os.listdir('./filtered/'):
        if file_name.endswith('.txt'):
            with open('./filtered/' + str(file_name)) as f:
                book = str(unicode(f.read(), errors="ignore"))
                cursor.execute("INSERT INTO books(book) VALUES (%s)", book)
                cursor.execute("INSERT INTO books_fulltext_index(book) VALUES (%s)", book)
                connection.commit()

def add_fulltext_index(connection, cursor):
    cursor.execute("ALTER TABLE books_fulltext_index ENGINE = MyISAM")
    cursor.execute("ALTER TABLE books_fulltext_index ADD FULLTEXT fulltext_index(book)")
    connection.commit()

if __name__ == "__main__":

    try:
        connection = MySQLdb.connect(db=config.db, user=config.user, passwd=config.password, host=config.host, use_unicode=True, charset="utf8")
        cursor = connection.cursor()

        setup_database(connection, cursor)
        write_books(connection, cursor)
        add_fulltext_index(connection, cursor)

    except MySQLdb.Error, e:
        try:
            print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
        except IndexError:
            print "MySQL Error: %s" % str(e)

    finally:
        if connection:
            connection.close()
