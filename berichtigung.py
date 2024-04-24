import csv
from tabulate import tabulate
import pandas as pd


class Serializer:
    def __init__(self):
        self.brutto_data: dict[str, list] = {}
        self.netto_data: dict[str, list] = {}
        self.years: list[str] = []

        self.percentages: dict[str, list[float]] = {}
        self.average: dict[str, float] = {}
        self.self_supply: dict[str, float] = {}

    def read_csv(self):
        with open("./data/netto.csv", "r", encoding="utf-8") as netto, open(
                "./data/brutto.csv", "r", encoding="utf-8") as brutto:
            netto_reader = csv.reader(netto, delimiter=";")
            brutto_reader = csv.reader(brutto, delimiter=";")

            self.process_netto(netto_reader)
            self.process_brutto(brutto_reader)

    def process_netto(self, reader):
        for i, data in enumerate(reader):
            if i == 0:
                self.years = data[1:]
                continue
            self.netto_data[data[0]] = data[1:]
            self.percentages[data[0]] = []

    def process_brutto(self, reader):
        for i, data in enumerate(reader):
            if i == 0:
                continue
            self.brutto_data[data[0]] = data[1:]

    def clean_up(self):
        for key in self.brutto_data.keys():
            self.brutto_data[key] = [string.replace(".", "").replace(",", ".") for string in self.brutto_data[key]]
            self.netto_data[key] = [string.replace(".", "").replace(",", ".") for string in self.netto_data[key]]

    def calc_percentages(self):
        for i, year in enumerate(self.years):
            year_sum: float = 0.0
            for key, value in self.netto_data.items():
                year_sum += float(value[i])
            for key, value in self.netto_data.items():
                self.percentages[key].append(float(value[i]) / year_sum * 100 if value[i] != "0" else 0)

    def calc_averages(self):
        for key, value in self.percentages.items():
            self.average[key] = sum(value) / len(value)

    #Aufgabe 3
    def calc_self_supply(self):
        for n_key, n_value in self.netto_data.items():
            percentages = []
            for i, value in enumerate(n_value):
                if self.brutto_data[n_key][i] != "0":
                    percentages.append(100 - (float(n_value[i]) / float(self.brutto_data[n_key][i]) * 100))
            self.self_supply[n_key] = sum(percentages) / len(percentages)

    def create_table(self):
        header = self.years
        header.insert(0, "Art")
        header.append("Anteil (Mittelwert)")
        header.append("Anteil Eigenbedarf (Mittelwert)")

        rows = []
        for key, value in self.percentages.items():
            row: list[str] = [f"{val:.2f}%" for val in value]
            row.insert(0, key)
            row.append(f"{self.average[key]:.2f}%")
            row.append(f"{self.self_supply[key]:.2f}%")
            rows.append(row)

        df = pd.DataFrame(rows)

        table = tabulate(rows, headers=header, stralign="center", tablefmt="pretty")
        with open("result.txt", "w") as result:
            result.write(table)
        df.to_excel("result.xlsx", header=header, index=False)

    def test(self):
        for i, year in enumerate(self.years):
            for key, value in self.netto_data.items():
                print(f"Year {year} at index {i}: Key is {key} and value is {value[i]}")

    def test2(self):
        for key, value in self.netto_data.items():
            print(key)
            for val in value:
                print(val)

    def run(self):
        self.read_csv()
        self.clean_up()

        self.calc_percentages()
        self.calc_averages()
        self.calc_self_supply()

        self.create_table()


if __name__ == "__main__":
    serializer = Serializer()
    serializer.run()
