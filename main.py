import requests
import selectorlib
from send_email import Email
import time
import sqlite3


# URL AND HEADERS INFORMATION
URL = "https://programmer100.pythonanywhere.com/tours"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/39.0.2171.95 Safari/537.36'}


# SCRAPE AND EXTRACT THE DATA
class Event:
    def scrape(self, url):
        """ Scrape the page source from the url parameter"""
        response = requests.get(url, headers=HEADERS)
        source = response.text
        return source


    def extract(self, source):
        """ Filter out the specific tours information from the entire scraped data  """
        extractor = selectorlib.Extractor.from_yaml_file('extract.yaml')
        value = extractor.extract(source)['tours']
        return value


# READ AND STORE THE DATA FROM THE DATABASE
class Database:

    def __init__(self, database_path):
        self.connection = sqlite3.connect(database_path)
        print('__init__ has been executed')

    def read(self, extracted):
        """ 1) Split extracted string into band, city & row.
            2) Query database to return any row with these 3 values"""

        row = extracted.split(",")
        row = [item.strip() for item in row]  # remove any leading or trailing spaces
        band, city, date = row

        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM events WHERE band=? AND city=? AND date=?",
                       (band, city, date))
        rows = cursor.fetchall()
        print(row)
        return rows


    def store(self, extracted):
        row = extracted.split(",")
        row = [item.strip() for item in row]
        cursor = self.connection.cursor()
        cursor.execute("INSERT INTO events VALUES(?,?,?)", row)
        self.connection.commit()


# EXECUTIVE FUNCTON
if __name__ == '__main__':
    while True:
        event = Event()
        scraped = event.scrape(URL)
        extracted = event.extract(scraped)
        print('Line 68:' + extracted)

        if extracted != "No upcoming tours":
            database = Database(database_path='data.db')
            row = database.read(extracted)
            if not row:
                # if list in not empty then it already exists in the database, so it needs to be added.
                database.store(extracted)
                email = Email()
                email.send(extracted)
        time.sleep(2)

