import argparse
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()


class Station(Base):
    __tablename__ = 'stations'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)


class Rental(Base):
    __tablename__ = 'rentals'
    id = Column(Integer, primary_key=True)
    bike_id = Column(Integer, nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    start_station_id = Column(Integer, ForeignKey('stations.id'), nullable=False)
    end_station_id = Column(Integer, ForeignKey('stations.id'), nullable=False)
    duration = Column(Integer)

    start_station = relationship('Station', foreign_keys=[start_station_id])
    end_station = relationship('Station', foreign_keys=[end_station_id])


def create_database(database):
    eng = create_engine(f'sqlite:///{database}.sqlite3')
    Base.metadata.create_all(eng)
    print(f"Created {database}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Create a SQLite database for bike rentals.')
    parser.add_argument('database_name', help='The name of the database to create')

    args = parser.parse_args()
    create_database(args.database_name)

