import urllib2
import os
import time


class BookFetcher:
    def __init__(self, skip_existing_files=True, sleep_timer=10):
        self.url = "https://www.gutenberg.org/files/"
        self.output_directory = "downloads/"
        self.skip_existing_files = skip_existing_files
        self.sleep_timer = sleep_timer

    def run(self, from_id=1, to_id=50):
        if not os.path.exists(self.output_directory):
            os.makedirs(self.output_directory)

        try:
            for index in range(from_id, to_id):
                file_name = str(index) + ".txt"

                if os.path.exists(self.output_directory + file_name) & self.skip_existing_files:
                    print "File " + file_name + " already fetched!"
                    continue

                response = urllib2.urlopen(self.url + str(index) + "/" + file_name)
                print response.info().type

                # stop when captcha is returned not to get blocked
                if response.info().type != "text/plain":
                    raise Exception("Server returned Captcha. Stopping now.")

                book = response.read()

                with open(self.output_directory + file_name, "w") as f:
                    print "Writing " + file_name
                    f.write(book)

                print "Waiting for " + str(self.sleep_timer) + " seconds..."
                time.sleep(self.sleep_timer)

        except Exception as e:
            print e
            exit(1)

if __name__ == "__main__":
    bf = BookFetcher()
    bf.run()
