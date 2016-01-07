class Helper:
    def __init__(self):
        self.book_directory = "downloads/"

    def write_file(self, book, filename):
        with open(self.book_directory + filename, "w") as f:
            print "Writing " + filename
            f.write(book)

        print "Book successfully written to disk."
