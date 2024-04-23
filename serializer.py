import csv
import texttable
from tabulate import tabulate# type: ignore[import-untyped]

brutto_data: dict[str, list[str]] = {}
netto_data: dict[str, list[str]] = {}
years: list[str]
total_percentages: dict[str, list[float]] = {}
self_supply_percentages: dict[str, list[float]] = {}
averages: dict[str, float] = {}

t = texttable.Texttable(0)
t.set_precision(2)

def extract_brutto_data(brutto_data, brutto_reader):
    for i, line in enumerate(brutto_reader):
        if i == 0:
            years = line[1:]
            continue
        brutto_data[line[0]] = line[1:]
    return years

def extract_netto_data(netto_data, total_percentages, netto_reader):
    for i, line in enumerate(netto_reader):
        if i == 0:
            continue
        netto_data[line[0]] = line[1:]
        total_percentages[line[0]] = []


with open("./data/brutto.csv", "r", encoding="utf-8", newline="") as brutto, open("./data/netto.csv", "r", encoding="utf-8") as netto:
    brutto_reader = csv.reader(brutto, delimiter=";")
    netto_reader = csv.reader(netto, delimiter=";")

    years = extract_brutto_data(brutto_data, brutto_reader)

    extract_netto_data(netto_data, total_percentages, netto_reader)

# Remove 1000's decimal point
for key in brutto_data.keys():
    brutto_data[key] = [string.replace(".", "").replace(",", ".") for string in brutto_data[key]]
    netto_data[key] = [string.replace(".", "").replace(",", ".") for string in netto_data[key]]

# Get all percentages of production
for i, year in enumerate(years):
    year_sum = 0.0
    for key, data in netto_data.items():
        year_sum += float(data[i])
    for key, data in netto_data.items():
        total_percentages[key].append(float(data[i]) / year_sum * 100 if data[i] != "0" else 0)

# Get the total average
for name, values in total_percentages.items():
    averages[name] = sum(values) / len(values)

# Get the percentage that is needed to supply itself
for key, n_data in netto_data.items():
    self_supply_percentages[key] = []
    b_data = brutto_data[key]
    for i, val in enumerate(n_data):
        if val == "0":
            continue
        self_supply_percentages[key].append(100 - (float(val) / float(b_data[i]) * 100))

# Create the table head
head = years.copy()
head.insert(0, "Art")
head.append("Anteil (Mittelwert)")
head.append("Eigenbedarf (Mittelwert)")
table = []

# Add table data
for name in netto_data.keys():
    table_row: list[str] = [f"{val:.2f}%" for val in total_percentages[name]]
    table_row.insert(0, name)
    table_row.append(f"{averages[name]:.2f}%")
    table_row.append(f"{sum(self_supply_percentages[name]) / len(self_supply_percentages[name]):.2f}%")
    table_row = [val.replace(".", ",") for val in table_row]
    table.append(table_row)

# Save data into file
with open("result.txt", "w", encoding="utf-8") as f:
    output = tabulate(table, headers=head)
    if isinstance(output, str):
        f.write(output)
