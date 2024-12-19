from flask import Blueprint

from local_import.init import db
from local_import.models import *

db_commands = Blueprint("db", __name__)

@db_commands.cli.command("create")
def create_tables():
    db.create_all()
    print("Tables created")

@db_commands.cli.command("drop")
def drop_tables():
    db.drop_all()
    print("Tables dropped")

@db_commands.cli.command("seed")
def seed_tables():

    venues = [
        Venue(
            name="Venue Sample 1",
            phone="0712 345 678"
        ),
        Venue(
            name="Venue Sample 2",
            phone="0798 765 432"
        )
    ]
    db.session.add_all(venues)

    guests = [
        Guest(
            name="Guest Sample 1",
            phone="0412 345 678",
            email="sample1@guest.com"
        ),
        Guest(
            name="Guest Sample 2",
            phone="0498 765 432",
            email="sample2@guest.com"
        )
    ]
    db.session.add_all(guests)

    db.session.commit()

    bookings = [
        Booking(
            guest_id=1,
            num_guests=2,
            time="2024-08-27"
        ),
        Booking(
            guest_id=2,
            num_guests=4,
            time="2024-08-27"
        )
    ]
    db.session.add_all(bookings)

    tables = [
        Table(
            table_number=1,
            max_guests=4,
            venue_id=1
        ),
        Table(
            table_number=2,
            max_guests=2,
            venue_id=1
        ),
        Table(
            table_number=1,
            max_guests=2,
            venue_id=2
        ),
        Table(
            table_number=2,
            max_guests=2,
            venue_id=2
        )
    ]
    db.session.add_all(tables)

    db.session.commit()

    bookings_tables = [
        BookingTable(
            booking_id=1,
            table_id=2
        ),
        BookingTable(
            booking_id=2,
            table_id=3
        ),
        BookingTable(
            booking_id=2,
            table_id=4
        )
    ]
    db.session.add_all(bookings_tables)

    db.session.commit()

    print("Tables seeded")