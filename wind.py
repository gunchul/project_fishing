from datetime import datetime
from bs4 import BeautifulSoup
import json

def timestamp_to_string(timestamp):
    timestamp -= 60*60*10
    dt_object = datetime.fromtimestamp(timestamp)
    return dt_object.strftime('%m-%d (%a) %H:%M:%S')

class Wind:
    def __init__(self, html):
        self.data = self._data_load(html)
        self.rows = {}
        self._wind_get()

    def _data_load(self, html):
        soup = BeautifulSoup(html, "html.parser")
        script = soup.find("script", string=lambda s: "ww.data.graphs" in s).string.split(";")[0]
        value_of_graphs = script.split('ww.data.graphs = ')[1]
        value_of_data = value_of_graphs.split('data:')[1].strip()[:-3]
        return json.loads(value_of_data)

    def _wind_add(self, x, wind, direction):
        if x not in self.rows:
            self.rows[x] = {}
        self.rows[x]["wind"] = wind
        self.rows[x]["direction"] = direction

    def _wind_get(self):
        groups = self.data["forecastGraphs"]["wind"]["dataConfig"]["series"]["groups"]
        for group in groups:
            for point in group["points"]:
                self._wind_add(point['x'], point['y'], point['directionText'])
    def export(self, db, region):
        for row in self.rows:
            sql = """
INSERT INTO wind(date, region, expected_timestamp, speed, direction) VALUES (%s, %s, %s, %s, %s);
"""
            values = (
                datetime.now(),
                region,
                row,
                self.rows[row]['wind'],
                self.rows[row]['direction']
            )
            db.insert(sql, values)

    def print(self):
        for row in self.rows:
            print(timestamp_to_string(row), self.rows[row]['wind'], self.rows[row]['direction'])

def test_wind_get():
    with open("data/wind.html", "r") as f:
        content = f.read()
    wind = Wind(content)
    wind.print()

if __name__ == "__main__":
    test_wind_get()
