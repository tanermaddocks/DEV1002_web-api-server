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

    print("Tables seeded")