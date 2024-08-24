from bs4 import BeautifulSoup
from datetime import datetime

class Moon:
    def __init__(self, html):
        self.rows = {}
        self._data_get(html)

    def _data_get(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        try:
            soup = soup.select("body > section > section.content > main > article > section.forecast > div > ul")[0]
            for li in soup.find_all('li', recursive=False):
                datetime = li.find('time').get('datetime')
                figure = li.find('figure').get("data-fill")
                self.rows[datetime] = {"figure":figure}
        except Exception as e:
            with open("log/error_moon.html", "wb") as f:
                f.write(html)
                raise e

    def export(self, db, region):
        for row in self.rows:
            sql = """
INSERT INTO moon(date, region, expect_date, amount) VALUES (%s, %s, %s, %s);
"""
            values = (
                datetime.now(),
                region,
                row,
                self.rows[row]['figure']
            )
            db.insert(sql, values)

    def print(self):
        for row in self.rows:
            print(row, self.rows[row]['figure'])

def test_moon_get():
    with open("data/moon.html", "rb") as f:
        content = f.read()
    moon = Moon(content)
    moon.print()

if __name__ == "__main__":
    test_moon_get()
