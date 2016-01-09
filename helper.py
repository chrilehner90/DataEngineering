import os

class Helper:
    def __init__(self):
        self.directory_original_books = "downloads/"
        self.directory_filtered_book = "filtered/"
        self.stemming_directory = "stemming/"
        self.lemmatization_directory = "lemmatization/"

    def read_file(self, filename):
        with open(self.directory_original_books + filename, "r") as f:
            return unicode(f.read(), errors="ignore")

    def write_file(self, book, filename, dest=""):
        directory = self.directory_original_books

        if not os.path.exists(self.directory_original_books):
            os.makedirs(self.directory_original_books)
        if not os.path.exists(self.directory_filtered_book):
            os.makedirs(self.directory_filtered_book)
        if not os.path.exists(self.stemming_directory):
            os.makedirs(self.stemming_directory)
        if not os.path.exists(self.lemmatization_directory):
            os.makedirs(self.lemmatization_directory)

        if dest == "f":
            directory = self.directory_filtered_book
        elif dest == "s":
            directory = self.stemming_directory
        elif dest == "l":
            directory = self.lemmatization_directory

        with open(directory + filename, "w") as f:
            print "Writing " + filename
            f.write(book)

        print "Book successfully written to", directory + filename
