import argparse
import os
from load_data import load_data


def load_all_data(directory, database):
    for month in range(1, 13):
        file_name = f"historia_przejazdow_2021-{month:02d}.csv"
        file_path = os.path.join(directory, file_name)

        if os.path.isfile(file_path):
            print(f"Ładowanie danych z pliku: {file_path}")
            load_data(file_path, database)
        else:
            print(f"Plik {file_path} nie istnieje.")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Load station and rental data from multiple CSV files into SQLite database.')
    parser.add_argument('directory', help='Directory containing CSV files')
    parser.add_argument('database_name', help='Name of the SQLite database')

    args = parser.parse_args()
    load_all_data(args.directory, args.database_name)