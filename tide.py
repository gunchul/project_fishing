from datetime import datetime
from bs4 import BeautifulSoup

class Tide:
    def __init__(self, html):
        self.rows = {}
        self._data_get(html)

    def _data_get(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        soup = soup.select("body > section > section.content > main > article > section > div > ul")[0]
        for li in soup.find_all('li', recursive=False):
            datetime = li.find('time').get('datetime')
            self.rows[datetime] = []
            for subli in li.find('ul').find_all('li'):
                time = subli.find('h3').text
                height = subli.find('span').text
                self.rows[datetime].append({"time":time, "height":height})

    def export(self, db, region):
        for row in self.rows:
            for tuple in self.rows[row]:
                tide_datetime = f'{row} {tuple["time"]}'
                tide_datetime_obj = datetime.strptime(tide_datetime, '%Y-%m-%d %I:%M %p')
                sql = """
INSERT INTO tide(date, region, expect_date, time, height) VALUES (%s, %s, %s, %s, %s);
    """
                values = (
                    datetime.now(),
                    region,
                    row,
                    tide_datetime_obj,
                    tuple["height"].split("m")[0]
                )
                db.insert(sql, values)

    def print(self):
        for row in self.rows:
            print(row, self.rows[row])

def test_tide_get():
    with open("data/tide.html", "r") as f:
        content = f.read()
    tide = Tide(content)
    tide.print()

if __name__ == "__main__":
    test_tide_get()
