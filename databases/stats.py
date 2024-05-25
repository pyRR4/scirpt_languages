import argparse
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from create_database import Rental, Station, Base


def calc_stats(station_name, database):
    engine = create_engine(f'sqlite:///{database}.sqlite3')
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    session = DBSession()

    station = session.query(Station).filter(Station.name == station_name).first()
    if not station:
        print("Nie znaleziono stacji o podanej nazwie.")
        return

    avg_start_duration = (session.query(func.avg(Rental.duration)).
                          filter(Rental.start_station_id == station.id)
                          .scalar())

    avg_end_duration = (session.query(func.avg(Rental.duration)).
                        filter(Rental.end_station_id == station.id)
                        .scalar())

    bikes_count = (session.query(func.count(func.distinct(Rental.bike_id))).
                   filter(Rental.start_station_id == station.id)
                   .scalar())

    most_common_destination = (session.query(Station.name, func.count(Rental.end_station_id).label('count'))
                               .join(Rental, Rental.end_station_id == Station.id)
                               .filter(Rental.start_station_id == station.id)
                               .group_by(Station.name)
                               .order_by(func.count(Rental.end_station_id).desc())
                               .first())

    all_count = session.query(func.count(Rental.id)).scalar()

    session.close()

    return avg_start_duration, avg_end_duration, bikes_count, most_common_destination, all_count


def print_stats(station_name, database):
    stats = calc_stats(station_name, database)

    if stats:
        print(f"Średni czas trwania przejazdu rozpoczynanego na stacji {station_name}: {stats[0]:.2f} minut")
        print(f"Średni czas trwania przejazdu kończonego na stacji {station_name}: {stats[1]:.2f} minut")
        print(f"Liczba różnych rowerów parkowanych na stacji {station_name}: {stats[2]}")
        print(f"Stacja, do której najczęściej udawano się ze stacji {station_name}: {stats[3][0]} "
              f"({stats[3][1]} przejazdów)")
        print(f"Liczba wszystkich rekordów w tabeli Rental: {stats[4]}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Calculate statistics for a given station.')
    parser.add_argument('station_name', help='The name of the station')
    parser.add_argument('database_name', help='The name of the SQLite database')

    args = parser.parse_args()
    print_stats(args.station_name, args.database_name)

