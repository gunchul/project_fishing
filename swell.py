from datetime import datetime
from bs4 import BeautifulSoup
import json

def timestamp_to_string(timestamp):
    timestamp -= 60*60*10
    dt_object = datetime.fromtimestamp(timestamp)
    return dt_object.strftime('%m-%d (%a) %H')

class Swell:
    def __init__(self, html):
        self.data = self._data_load(html)
        self.rows = {}
        self._swell_height_get()
        self._swell_period_get()

    def _data_load(self, html):
        soup = BeautifulSoup(html, "html.parser")
        try:
            script = soup.find("script", string=lambda s: "ww.data.graphs" in s).string.split(";")[0]
            value_of_graphs = script.split('ww.data.graphs = ')[1]
            value_of_data = value_of_graphs.split('data:')[1].strip()[:-3]
        except Exception as e:
            with open("log/error_swell.html", "wb") as f:
                f.write(html)
                raise e

        return json.loads(value_of_data)

    def _swell_height_add(self, x, height, direction):
        if x not in self.rows:
            self.rows[x] = {}
        self.rows[x]["height"] = height
        self.rows[x]["direction"] = direction

    def _swell_period_add(self, x, period):
        if x not in self.rows:
            return
        self.rows[x]["period"] = period

    def _swell_height_get(self):
        groups = self.data["forecastGraphs"]["swell-height"]["dataConfig"]["series"]["groups"]
        for group in groups:
            for point in group["points"]:
                self._swell_height_add(point['x'], point['y'], point['directionText'])

    def _swell_period_get(self):
        groups = self.data["forecastGraphs"]["swell-period"]["dataConfig"]["series"]["groups"]
        for group in groups:
            for point in group["points"]:
                self._swell_period_add(point['x'], point['y'])

    def export(self, db, region):
        for row in self.rows:
            if "period" not in self.rows[row]:
                continue
            sql = """
INSERT INTO swell(date, region, expected_timestamp, height, direction, period) VALUES (%s, %s, %s, %s, %s, %s);
"""
            values = (
                datetime.now(),
                region,
                row,
                self.rows[row]['height'],
                self.rows[row]['direction'],
                self.rows[row]['period']
            )
            db.insert(sql, values)

    def print(self):
        for row in self.rows:
            if "period" not in self.rows[row]:
                continue
            print(timestamp_to_string(row), self.rows[row]['height'], self.rows[row]['direction'], self.rows[row]['period'])

def test_swell_get():
    with open("data/swell.html", "rb") as f:
        content = f.read()
    swell = Swell(content)
    swell.print()

if __name__ == "__main__":
    test_swell_get()
