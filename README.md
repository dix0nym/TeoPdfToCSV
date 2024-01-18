# TeoPdfToCSV

A simple python script to parse the monthly bank statement pdf (Kontoauszug) of Teo Web/Sparda Bank to CSV.

## Installation

```bash
# clone and install repo
git clone https://github.com/dix0nym/TeoPdfToCSV
cd TeoPdfToCSV

# install requirements via pipenv
pipenv install

# install pipenv before if necessary
pip install pipenv --user

# install requirements via pip
pip install --user -r requirements.txt
```

## Usage

```bash
usage: TeoPdfToCSV [-h] [-o OUTPUT] input

positional arguments:
  input                 input, can be either a file or directoyr

options:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        output folder
```

Examples:

```bash
# process single file
pipenv run python teoPdfToCSV.py bank_statement.pdf

# process single file and write to output
pipenv run python teoPdfToCSV.py -o output\ bank_statement.pdf

# process all files in "input\" and write CSVs to "output\"
pipenv run python teoPdfToCSV.py -o output\ input\
```

## CSV Structure

The generated CSV has the following structure:

```csv
Buchungstag,Name,Buchungstext,Wertstellung,Betrag
01.01.2024,Max Mustermann,Max Mustermann SEPA-BASISLASTSCHRIFT,01.01.2024,-100,00
```

## Requirements

- [tabula-py](https://pypi.org/project/tabula-py/)
- [pandas](https://pypi.org/project/pandas/)
- (only tested on Python 3.10.5)

## FireflyIII

Using the provided [import config](./fireflyIII_import_config.json) the generated CSV files
can be directly imported in [fireFlyIII](https://www.firefly-iii.org/).
