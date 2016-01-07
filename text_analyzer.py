import os

from helper import Helper


class TextAnalyzer:
    def __init__(self):
        self.Helper = Helper()

    def run(self):
        for f in os.listdir(self.Helper.book_directory):
            if f.endswith(".txt"):
                book = self.Helper.read_file(f)

if __name__ == "__main__":
    ta = TextAnalyzer()
    ta.run()
