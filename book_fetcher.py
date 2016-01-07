import urllib2
import os
import time

from helper import Helper


class BookFetcher:
    def __init__(self, skip_existing_files=True, sleep_timer=10):
        self.Helper = Helper()
        self.url = "https://www.gutenberg.org/files/"
        self.skip_existing_files = skip_existing_files
        self.sleep_timer = sleep_timer

        self.ignored_books = [69]

    def run(self, from_id=1, to_id=100):

        try:
            for index in range(from_id, to_id):
                filename = str(index) + ".txt"

                if os.path.exists(self.Helper.book_directory + filename) & self.skip_existing_files:
                    print "File " + filename + " already fetched!"
                    continue

                if index in self.ignored_books:
                    continue

                response = urllib2.urlopen(self.url + str(index) + "/" + filename)

                if response.info().type != "text/plain":
                    raise Exception("Server returned Captcha. Stopping now.")

                book = response.read()

                self.Helper.write_file(book, filename)

                print "Waiting for " + str(self.sleep_timer) + " seconds..."
                time.sleep(self.sleep_timer)

        except urllib2.HTTPError as err:
            # if a book is not found (i.e. HTTP status code is 404) then try the next book
            if err.code == 404:
                self.run(index + 1, to_id)
        except Exception as err:
            # stop when captcha is returned not to get blocked
            print err
            exit(1)

if __name__ == "__main__":
    bf = BookFetcher()
    bf.run()
