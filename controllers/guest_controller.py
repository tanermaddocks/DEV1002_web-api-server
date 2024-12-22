from flask import Blueprint, request
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes

from local_import.init import db
from models.guest import Guest, guests_schema, guest_schema

guest_bp = Blueprint("guests", __name__, url_prefix="/guests")

# Create - /guests - POST
@guest_bp.route("/", methods=["POST"])
def create_guest():
    # integrity error try/except for unique and not_null violations
    try:
        # get data from body
        body_data = guest_schema.load(request.get_json(), partial=True)
        # create instance
        new_guest = Guest(
            name = body_data.get("name"),
            phone = body_data.get("phone"), 
            email = body_data.get("email")
        )
        # add to session
        db.session.add(new_guest)
        # commit new object
        db.session.commit()
        # return new object
        return guest_schema.dump(new_guest), 201
    except IntegrityError as err:
        # check for error not_null
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            # return error message
            return {"message": f"The field '{err.orig.diag.column_name}' is required"}, 409
        # check for error unique
        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
            # return error message
            return {"message": f"Guest {err.orig.diag.column_name} already in use"}, 409

# Read all - /guests - GET
@guest_bp.route("/")
def get_guests():
    # return all items in table
    return guests_schema.dump(db.session.scalars(db.select(Guest)))


# Read one - /guests/id - GET
@guest_bp.route("/<int:guest_id>/")
def get_guest(guest_id):
    # load object data from id
    guest = db.session.scalar(db.select(Guest).filter_by(guest_id=guest_id))
    # check guest exists
    if guest:
        # return requested object data
        return guest_schema.dump(guest)
    else:
        # return error message
        return {"message": f"Guest with id {guest_id} does not exist"}, 404

# Update - /guests/id - PUT, PATCH
@guest_bp.route("/<int:guest_id>/", methods=["PUT", "PATCH"])
def update_guest(guest_id):
    # integrity error try/except for unique violations
    try:
        # load object data from id
        guest = db.session.scalar(db.select(Guest).filter_by(guest_id=guest_id))
        # load input data
        body_data = guest_schema.load(request.get_json(), partial=True)
        # check guest exists
        if guest:
            # assign new values or use old ones
            guest.name = body_data.get("name") or guest.name
            guest.phone = body_data.get("phone") or guest.phone
            guest.email = body_data.get("email") or guest.email
            # commit changes
            db.session.commit()
            # return new object
            return guest_schema.dump(guest)
        # if no guest
        else:
            # return error message
            return {"message": f"Guest with id {guest_id} does not exist"}, 404
    except IntegrityError as err:
        # check for error unique
        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
            # return error message
            return {"message": f"Guest {err.orig.diag.column_name} already in use"}, 409

# Delete - /guests/id - DELETE
@guest_bp.route("/<int:guest_id>/", methods=["DELETE"])
def delete_guest(guest_id):
    # load object data from id
    guest = db.session.scalar(db.select(Guest).filter_by(guest_id=guest_id))
    # check guest exists
    if guest:
        # delete the object
        db.session.delete(guest)
        # commit to session
        db.session.commit()
        # return successful
        return {"message": f"Guest '{guest.name}' deleted successfully"}
    # if no guest
    else:
        # return error message
        return {"message": f"Guest with id {guest_id} does not exist"}, 404