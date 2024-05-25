import argparse
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from create_database import Station, Rental, Base
from datetime import datetime


def load_data(csv_file, database):
    engine = create_engine(f'sqlite:///{database}.sqlite3')
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    session = DBSession()

    data = pd.read_csv(csv_file)
    station_id_map = {}
    all_stations = set(data['Stacja wynajmu']).union(set(data['Stacja zwrotu']))

    for station_name in all_stations:
        station = session.query(Station).filter_by(name=station_name).first()
        if not station:
            station = Station(name=station_name)
            session.add(station)
            session.flush()
        station_id_map[station_name] = station.id

    for index, row in data.iterrows():
        rental_id = row['UID wynajmu']
        existing_rental = session.query(Rental).filter_by(id=rental_id).first()

        if existing_rental:
            print(f"Rekord o id {rental_id} już istnieje, pomijanie.")
            continue

        start_time_datetime = datetime.strptime(row['Data wynajmu'], '%Y-%m-%d %H:%M:%S')
        end_time_datetime = datetime.strptime(row['Data zwrotu'], '%Y-%m-%d %H:%M:%S')

        rental = Rental(
            id=row['UID wynajmu'],
            bike_id=row['Numer roweru'],
            start_time=start_time_datetime,
            end_time=end_time_datetime,
            start_station_id=station_id_map[row['Stacja wynajmu']],
            end_station_id=station_id_map[row['Stacja zwrotu']],
            duration=row['Czas trwania']
        )
        session.add(rental)

    session.commit()
    session.close()

    print(f"Zaladowano dane do bazy {database}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Load station and rental data from CSV file into SQLite database.')
    parser.add_argument('csv_file', help='CSV file containing station and rental data')
    parser.add_argument('database_name', help='Name of the SQLite database')

    args = parser.parse_args()
    load_data(args.csv_file, args.database_name)

