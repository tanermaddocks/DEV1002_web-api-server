from flask import Blueprint, request
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes

from local_import.init import db
from models.booking import Booking, bookings_schema, booking_schema

booking_bp = Blueprint("bookings", __name__, url_prefix="/bookings")

# Create - /bookings - POST
@booking_bp.route("/", methods=["POST"])
def create_booking():
    # integrity error try/except for not_null violations
    try:
        # get data from body
        body_data = request.get_json()
        # create instance
        new_booking = Booking(
            num_guests = body_data.get("num_guests"),
            guest_id = body_data.get("guest_id"),
            booking_date = body_data.get("booking_date")
        )
        # add to session
        db.session.add(new_booking)
        # commit new object
        db.session.commit()
        # return new object
        return booking_schema.dump(new_booking), 201
    except IntegrityError as err:
        # check for error not_null
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            # return error message
            return {"message": f"The field '{err.orig.diag.column_name}' is required"}, 409


# Read all - /bookings - GET
@booking_bp.route("/")
def get_bookings():
    # return all items in booking
    return bookings_schema.dump(db.session.scalars(db.select(Booking)))


# Read one - /bookings/id - GET
@booking_bp.route("/<int:booking_id>")
def get_booking(booking_id):
    # load object data from id
    booking = db.session.scalar(db.select(Booking).filter_by(id=booking_id))
    # check booking exists
    if booking:
        # return requested object data
        return booking_schema.dump(booking)
    else:
        # return error message
        return {"message": f"Booking with id {booking_id} does not exist"}, 404

# Update - /bookings/id - PUT, PATCH
@booking_bp.route("/<int:booking_id>", methods=["PUT", "PATCH"])
def update_booking(booking_id):
    # load object data from id
    booking = db.session.scalar(db.select(Booking).filter_by(id=booking_id))
    # load input data
    body_data = request.get_json()
    # body_data = booking_schema.load(request.get_json(), partial=True)
    # check booking exists
    if booking:
        # assign new values or use old ones
        booking.num_guests = body_data.get("num_guests") or booking.num_guests
        booking.guest_id = body_data.get("guest_id") or booking.guest_id
        booking.booking_date = body_data.get("booking_date") or booking.booking_date
        # commit changes
        db.session.commit()
        # return new object
        return booking_schema.dump(booking)
    # if no booking
    else:
        # return error message
        return {"message": f"Booking with id {booking_id} does not exist"}, 404

# Delete - /bookings/id - DELETE
@booking_bp.route("/<int:booking_id>", methods=["DELETE"])
def delete_booking(booking_id):
    # load object data from id
    booking = db.session.scalar(db.select(Booking).filter_by(id=booking_id))
    # check booking exists
    if booking:
        # delete the object
        db.session.delete(booking)
        # commit to session
        db.session.commit()
        # return successful
        return {"message": f"Booking with id {booking.id} deleted successfully"}
    # if no booking
    else:
        # return error message
        return {"message": f"Booking with id {booking_id} does not exist"}, 404