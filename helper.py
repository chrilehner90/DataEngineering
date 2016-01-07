import os

class Helper:
    def __init__(self):
        self.book_directory = "downloads/"
        self.stemming_directory = "stemming/"
        self.lemmatization_directory = "lemmatization/"

    def read_file(self, filename):
        with open(self.book_directory + filename, "r") as f:
            return unicode(f.read(), errors="ignore")

    def write_file(self, book, filename, dest=""):
        directory = self.book_directory

        if not os.path.exists(self.book_directory):
            os.makedirs(self.book_directory)
        if not os.path.exists(self.stemming_directory):
            os.makedirs(self.stemming_directory)
        if not os.path.exists(self.lemmatization_directory):
            os.makedirs(self.lemmatization_directory)

        if dest == "s":
            directory = self.stemming_directory
        elif dest == "l":
            directory = self.lemmatization_directory

        with open(directory + filename, "w") as f:
            print "Writing " + filename
            f.write(book)

        print "Book successfully written to disk."
