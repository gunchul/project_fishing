from datetime import datetime
from bs4 import BeautifulSoup
import json

def timestamp_to_string(timestamp):
    timestamp -= 60*60*10
    dt_object = datetime.fromtimestamp(timestamp)
    return dt_object.strftime('%m-%d (%a) %H:%M:%S')

class RainfallPossibility:
    def __init__(self, html):
        self.data = self._data_load(html)
        self.rows = {}
        self._rainfall_get()

    def _data_load(self, html):
        soup = BeautifulSoup(html, "html.parser")
        script = soup.find("script", string=lambda s: "ww.data.graphs" in s).string.split(";")[0]
        value_of_graphs = script.split('ww.data.graphs = ')[1]
        value_of_data = value_of_graphs.split('data:')[1].strip()[:-3]
        return json.loads(value_of_data)

    def _rainfall_add(self, x, rainfall):
        if x not in self.rows:
            self.rows[x] = {}
        self.rows[x]["rainfall"] = rainfall

    def _rainfall_get(self):
        groups = self.data["forecastGraphs"]["rainfallprobability"]["dataConfig"]["series"]["groups"]
        for group in groups:
            for point in group["points"]:
                self._rainfall_add(point['x'], point['y'])

    def export(self, db, region):
        for row in self.rows:
            sql = """
INSERT INTO rainfall_possibility(date, region, expected_timestamp, possibility) VALUES (%s, %s, %s, %s);
"""
            values = (
                datetime.now(),
                region,
                row,
                self.rows[row]['rainfall']
            )
            db.insert(sql, values)

    def print(self):
        for row in self.rows:
            print(timestamp_to_string(row), self.rows[row]['rainfall'])

class Rainfall:
    def __init__(self, html):
        self.rows = {}
        self._data_get(html)

    def _data_get(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        try:
            soup = soup.select("body > section > section.content > main > article > section.forecast.selectable > div > ul")[0]
            for li in soup.find_all('li'):
                datetime = li.find('time').get('datetime')
                percent = 0
                amount = 0
                for b in li.find_all('b'):
                    if "%" in b.text:
                        percent = b.text
                    elif "mm" in b.text:
                        amount = b.text
                self.rows[datetime] = {"percent":percent, "amount":amount}
        except Exception as e:
            with open("log/error_rainfall.html", "w") as f:
                f.write(html)
                raise e

    def export(self, db, region):
        for row in self.rows:
            sql = """
INSERT INTO rainfall(date, region, expect_date, possibility, amount) VALUES (%s, %s, %s, %s, %s);
"""
            values = (
                datetime.now(),
                region,
                row,
                self.rows[row]['percent'],
                self.rows[row]['amount'],
            )
            db.insert(sql, values)

    def print(self):
        for row in self.rows:
            print(row, self.rows[row]['percent'], self.rows[row]['amount'])

def test_rainfall_get():
    with open("data/rainfall.html", "r") as f:
        content = f.read()
    rainfall = RainfallPossibility(content)
    rainfall.print()
    rainfall_summary = Rainfall(content)
    rainfall_summary.print()

if __name__ == "__main__":
    test_rainfall_get()
