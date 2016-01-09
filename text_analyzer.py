import os
import nltk.data
from nltk.stem import SnowballStemmer
from nltk.stem import WordNetLemmatizer

nltk.download("wordnet")

from helper import Helper

class TextAnalyzer:
    def __init__(self):
        self.Helper = Helper()
        self.Stemmer = SnowballStemmer("english")
        self.Lemmatizer = WordNetLemmatizer()

        self.books = []
        self.stemmed_books = []
        self.lemmatized_books = []

        self.all_tokens_counts = []
        self.distinct_tokens_counts = []
        self.distinct_tokens_counts_with_stemming = []
        self.distinct_tokens_counts_with_lemmatization = []

    def process_text(self, specific_id = -1, perform_stemming=True, perform_lemmatization=True):
        for filename in os.listdir(self.Helper.directory_original_books):
            if filename.endswith(".txt"):
                # only analyze book with specific ID
                if (specific_id >= 0) & (filename != str(specific_id) + ".txt"):
                    continue
                book = self.Helper.read_file(filename)

                # analyze books without stemming
                tokens = self.tokenize(book)

                # join tokens again to have the filtered text for stemming
                book = " ".join(tokens)

                self.Helper.write_file(book, filename, "f")

                self.books.append(book)

                self.all_tokens_counts.append(len(tokens))

                self.distinct_tokens_counts.append(len(self.get_distinct_tokens(tokens)))

                if perform_stemming:
                    stemmed_book = self.perform_stemming(book, filename)
                    self.stemmed_books.append(stemmed_book)

                    self.Helper.write_file(stemmed_book, filename, "s")

                    stemmed_tokens = self.tokenize(stemmed_book)
                    self.distinct_tokens_counts_with_stemming.append(
                            len(self.get_distinct_tokens(stemmed_tokens))
                    )

                if perform_lemmatization:
                    lemmatized_book = self.perform_lemmatization(book, filename)
                    self.lemmatized_books.append(lemmatized_book)

                    self.Helper.write_file(lemmatized_book, filename, "l")

                    lemmatized_tokens = self.tokenize(lemmatized_book)
                    self.distinct_tokens_counts_with_lemmatization.append(
                            len(self.get_distinct_tokens(lemmatized_tokens))
                    )

    # tokenization currently without stopword removal
    def tokenize(self, string):
        book_lower_case = string.lower()
        tokens = nltk.wordpunct_tokenize(book_lower_case)
        tokens_filtered = filter(lambda t: t.isalpha(), tokens)

        return tokens_filtered

    def perform_stemming(self, book, filename):
        print "INFO: STEMMING", filename
        stemmed_book = ""
        for word in book.split():
            stemmed_word = self.Stemmer.stem(word)
            stemmed_book += stemmed_word + " "

        return stemmed_book

    def perform_lemmatization(self, book, filename):
        print "INFO: LEMMATIZING", filename
        lemmatized_book = ""
        for word in book.split():
            lemmatized_word = self.Lemmatizer.lemmatize(word)
            lemmatized_book += lemmatized_word + " "

        return lemmatized_book


    def get_distinct_tokens(self, tokens):
        return set(tokens)

    def get_document_count(self):
        return len(self.books)

    def count_all_tokens_of_all_books(self):
        return sum(self.all_tokens_counts)

    def count_distinct_tokens_of_all_books(self):
        return sum(self.distinct_tokens_counts)

    def count_distinct_tokens_of_all_books_with_stemming(self):
        return sum(self.distinct_tokens_counts_with_stemming)

    def count_distinct_tokens_of_all_books_with_lemmatization(self):
        return sum(self.distinct_tokens_counts_with_lemmatization)

    def calculate_zipf_distribution(self):
        return "TODO: Calculate Zipf distribution here"

if __name__ == "__main__":
    ta = TextAnalyzer()
    ta.process_text(perform_stemming=False, perform_lemmatization=False)

    print "# OF DOCUMENTS:", ta.get_document_count()
    print "# OF ALL TOKENS:", ta.count_all_tokens_of_all_books()
    print "# OF DISTINCT TOKENS:", ta.count_distinct_tokens_of_all_books()
    print "# OF DISTINCT TOKENS AFTER STEMMING:", ta.count_distinct_tokens_of_all_books_with_stemming()
    print "# OF DISTINCT TOKENS AFTER LEMMATIZATION:", ta.count_distinct_tokens_of_all_books_with_lemmatization()
    print "Zipf Distribution:", ta.calculate_zipf_distribution()