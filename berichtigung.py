import csv
from tabulate import tabulate

brutto_data: dict = {}
netto_data: dict = {}
total_percentages: dict[str, list[float]] = {}


def extract_brutto_data(reader, brutto_data):
    list_years: list[str] = []
    for i, line in enumerate(reader):
        if i == 0:
            list_years = line[1:]
        else:
            brutto_data[line[0]] = line[1:]
    return list_years


def extract_netto_data(reader, total_percentages, netto_data):
    for i, line in enumerate(reader):
        if i == 0:
            continue
        netto_data[line[0]] = line[1:]
        total_percentages[line[0]] = []


with open("./data/brutto.csv", "r", encoding="utf-8", newline="") as brutto, open("./data/netto.csv", "r", encoding="utf-8") as netto:
    brutto_reader = csv.reader(brutto, delimiter=";")
    netto_reader = csv.reader(netto, delimiter=";")

    years = extract_brutto_data(brutto_reader, brutto_data)
    extract_netto_data(netto_reader, total_percentages, netto_data)

for key in brutto_data.keys():
    brutto_data[key] = [string.replace(".", "").replace(",", ".") for string in brutto_data[key]]
    netto_data[key] = [string.replace(".", "").replace(",", ".") for string in netto_data[key]]

for i, year in enumerate(years):
    year_sum = 0.0
    for value in netto_data:
        year_sum += float(netto_data[value][i])
    for key, data in netto_data.items():
        total_percentages[key].append((float(data[i]) / year_sum * 100 if data[i] != "0" else 0))

mittelwerte = {}

for key, value in total_percentages.items():
    mittelwerte[key] = sum(value) / len(total_percentages[key])

header = years
header.insert(0, 'Art')
header.append('Mittelwerte')
rows = []

for name in netto_data.keys():
    row: list[str] = [f"{val:.2f}%" for val in total_percentages[name]]
    row.insert(0, name)
    row.append(f"{mittelwerte[name]:.2f}%")
    rows.append(row)

print(rows)
table = tabulate(rows, headers=header, tablefmt='github')
with open("result.txt", "w") as result:
    result.write(table)
