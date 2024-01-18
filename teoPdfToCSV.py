from tabula import read_pdf
import pandas
from pathlib import Path
import argparse


def getTable(page, df):
    row_start_locs = df.index[df["Wertstellung"] == "Wertstellung"]
    row_end_locs = df.loc[pandas.isna(df["Buchungstext"]), :].index

    row_start = min(row_start_locs.tolist()) + 2
    row_end = max(row_end_locs.tolist(), default=len(df))
    print(f"\tpage {page+1} - table@[{row_start},{row_end}]")

    df = df.iloc[:row_end]
    df = df.iloc[row_start:]

    df.reset_index(drop=True, inplace=True)
    return df


def concatDescriptions(df):
    entry_idx = df.loc[~df["Wertstellung"].isna()].index
    dfs = []
    for i, idx in enumerate(entry_idx):
        start_idx = idx
        current_df = df.copy()
        if i + 1 == len(entry_idx):
            current_df = current_df[start_idx:]
        else:
            current_df = current_df[:entry_idx[i+1]]
            current_df = current_df[start_idx:]
        current_df["Buchungstext"] = current_df["Buchungstext"].str.cat(
            sep=' ')
        current_df["Name"] = current_df["Buchungstext"].str.extract(
            "^(.*?)\sSEPA").fillna('')
        current_df = current_df.head(1)
        dfs.append(current_df)
    df = pandas.concat(dfs)
    df.reset_index(drop=True, inplace=True)
    return df


def extractTransactionDate(df):
    df = df.copy()
    df["Buchungstag"] = df["Buchungstext"].str.extract(
        '^(\d{2}\.\d{2}\.\d{4})\s').fillna('')
    df["Buchungstext"] = df["Buchungstext"].str.replace(
        '^(\d{2}\.\d{2}\.\d{4})\s', '', regex=True)
    return df


def parse(path, output):
    pages = read_pdf(path, pages="all", stream=True)
    all_df = []
    for page, df in enumerate(pages):
        df.columns = ["Buchungstext", "Wertstellung", "Betrag"]
        df = getTable(page, df)

        if df.empty:
            print(f"\ttable on page {page} is empty")
            continue

        df = extractTransactionDate(df)
        all_df.append(concatDescriptions(df))

    df = pandas.concat(all_df)
    df.to_csv(output, columns=[
              "Buchungstag", "Name", "Buchungstext", "Wertstellung", "Betrag"], index=False)
    return df


def handleDirectory(inputPath, outputPath):
    total_dfs = []
    for f in inputPath.glob("*.pdf"):
        print(f"processing {f}")
        ddf = parse(f, outputPath.joinpath(f.with_suffix(".csv").name))
        total_dfs.append(ddf)
    total_df = pandas.concat(total_dfs)
    total_df.to_csv("output_total.csv", columns=[
        "Buchungstag", "Name", "Buchungstext", "Wertstellung", "Betrag"], index=False)


def main():
    parser = argparse.ArgumentParser("TeoPdfToCSV")
    parser.add_argument("-o", "--output", type=Path,
                        default=Path("."), help="output folder")
    parser.add_argument("input", type=Path,
                        help="input, can be either a file or directoyr")
    args = parser.parse_args()

    inputPath = args.input
    outputPath = args.output
    if inputPath.is_dir():
        handleDirectory(inputPath, outputPath)
    else:
        print(f"processing {inputPath}")
        parse(inputPath, outputPath.joinpath(
            inputPath.with_suffix(".csv").name))


if __name__ == "__main__":
    main()
