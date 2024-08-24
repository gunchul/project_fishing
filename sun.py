from datetime import datetime
from bs4 import BeautifulSoup

class Sun:
    def __init__(self, html):
        self.rows = {}
        self._data_get(html)

    def _data_get(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        try:
            soup = soup.select("body > section > section.content > main > article > section.forecast > div > ul")[0]
            for li in soup.find_all('li', recursive=False):
                datetime = li.find('time').get('datetime')
                first_light = li.find(class_ = "first-light").find('span').text
                sunrise = li.find(class_ = "sunrise").find('span').text
                sunset = li.find(class_ = "sunset").find('span').text
                last_light = li.find(class_ = "last-light").find('span').text

                self.rows[datetime] = {"first_light":first_light,
                                    "sunrise":sunrise,
                                    "sunset":sunset,
                                    "last_light":last_light}
        except Exception as e:
            with open("log/error_sun.html", "w") as f:
                f.write(html)
                raise e

    def export(self, db, region):
        for row in self.rows:
            sql = """
INSERT INTO sun(date, region, expect_date, first_light, sunrise, sunset, last_light) VALUES (%s, %s, %s, %s, %s, %s, %s);
"""
            values = (
                datetime.now(),
                region,
                row,
                self.rows[row]['first_light'],
                self.rows[row]['sunrise'],
                self.rows[row]['sunset'],
                self.rows[row]['last_light']
            )
            db.insert(sql, values)

    def print(self):
        for row in self.rows:
            print(row, self.rows[row]['first_light'], self.rows[row]['sunrise'], self.rows[row]['sunset'], self.rows[row]['last_light'])

def test_sun_get():
    with open("data/sun.html", "r") as f:
        content = f.read()
    sun = Sun(content)
    sun.print()

if __name__ == "__main__":
    test_sun_get()
