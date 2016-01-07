import os
import nltk
from helper import Helper

# download tokenizers
nltk.download("punkt")

class TextAnalyzer:
    def __init__(self):
        self._Helper = Helper()
        self._document_count = 0
        self._all_tokens_counts = []

    def run(self):
        for f in os.listdir(self._Helper.book_directory):
            if f.endswith(".txt"):
                book = self._Helper.read_file(f)
                self._document_count += 1
                self._all_tokens_counts.append(len(self.tokenize(book)))

    def tokenize(self, book):
        book_lower_case = book.lower()
        tokens = nltk.wordpunct_tokenize(book_lower_case)
        tokens_filtered = filter(lambda t: t.isalnum(), tokens)

        return tokens_filtered

    def get_document_count(self):
        return self._document_count

    def count_all_tokens_of_all_books(self):
        return sum(self._all_tokens_counts)

if __name__ == "__main__":
    ta = TextAnalyzer()
    ta.run()

    print "# OF DOCUMENTS:", ta.get_document_count()
    print "ALL TOKENS:", ta.count_all_tokens_of_all_books()
