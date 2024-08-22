from datetime import datetime
from bs4 import BeautifulSoup
import json

def timestamp_to_string(timestamp):
    timestamp -= 60*60*10
    dt_object = datetime.fromtimestamp(timestamp)
    return dt_object.strftime('%m-%d (%a) %H:%M:%S')

class Temperature:
    def __init__(self, html):
        self.data = self._data_load(html)
        self.rows = {}
        self._weather_temperature_get()

    def _data_load(self, html):
        soup = BeautifulSoup(html, "html.parser")
        script = soup.find("script", string=lambda s: "ww.data.graphs" in s).string.split(";")[0]
        value_of_graphs = script.split('ww.data.graphs = ')[1]
        value_of_data = value_of_graphs.split('data:')[1].strip()[:-3]
        return json.loads(value_of_data)

    def _weather_temperature_add(self, x, temperature):
        if x not in self.rows:
            self.rows[x] = {}
        self.rows[x]["temperature"] = temperature

    def _weather_temperature_get(self):
        groups = self.data["forecastGraphs"]["temperature"]["dataConfig"]["series"]["groups"]
        for group in groups:
            for point in group["points"]:
                self._weather_temperature_add(point['x'], point['y'])

    def export(self, db, region):
        for row in self.rows:
            sql = """
INSERT INTO temperature(date, region, expected_timestamp, temperature) VALUES (%s, %s, %s, %s);
"""
            values = (
                datetime.now(),
                region,
                row,
                self.rows[row]['temperature']
            )
            db.insert(sql, values)

    def print(self):
        for row in self.rows:
            print(timestamp_to_string(row), self.rows[row]['temperature'])

def test_weather_get():
    with open("data/weather.html", "r") as f:
        content = f.read()
    weather = Temperature(content)
    weather.print()

if __name__ == "__main__":
    test_weather_get()
