import os

class Helper:
    def __init__(self):
        self.directory_original_books = "downloads/"
        self.directory_filtered_book = "filtered/"
        self.stemming_directory = "stemming/"
        self.lemmatization_directory = "lemmatization/"

    def get_directory(self, identifier):
        directory = self.directory_original_books

        if identifier == "f":
            directory = self.directory_filtered_book
        elif identifier == "s":
            directory = self.stemming_directory
        elif identifier == "l":
            directory = self.lemmatization_directory

        return directory

    def read_file(self, filename, identifier=""):
        directory = self.get_directory(identifier)
        with open(directory + filename, "r") as f:
            return unicode(f.read(), errors="ignore")

    def write_file(self, book, filename, identifier=""):
        directory = self.get_directory(identifier)

        if not os.path.exists(self.directory_original_books):
            os.makedirs(self.directory_original_books)
        if not os.path.exists(self.directory_filtered_book):
            os.makedirs(self.directory_filtered_book)
        if not os.path.exists(self.stemming_directory):
            os.makedirs(self.stemming_directory)
        if not os.path.exists(self.lemmatization_directory):
            os.makedirs(self.lemmatization_directory)

        if not os.path.exists(directory + filename):
            with open(directory + filename, "w") as f:
                print "Writing " + filename
                f.write(book)

            print "Book successfully written to", directory + filename
            return True
        else:
            print directory + filename, "already exists"
            return False
