from flask import Blueprint, request
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes

from init import db
from models.venue import Venue, venues_schema, venue_schema

venue_bp = Blueprint("venues", __name__, url_prefix="/venues")

# Create - /venues - POST
@venue_bp.route("/", methods=["POST"])
def create_venue():
    # integrity error try/except for unique and not_null violations
    try:
        # get data from body
        body_data = request.get_json()
        # create instance
        new_venue = Venue(
            name = body_data.get("name"),
            phone = body_data.get("phone")
        )
        # add to session
        db.session.add(new_venue)
        # commit new object
        db.session.commit()
        # return new object
        return venue_schema.dump(new_venue), 201
    except IntegrityError as err:
        # check for error not_null
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            # return error message
            return {"message": f"The field '{err.orig.diag.column_name}' is required"}, 409
        # check for error unique
        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
            # return error message
            return {"message": "Venue phone number already in use"}, 409

# Read all - /venues - GET
@venue_bp.route("/")
def get_venues():
    # return all items in table
    return venues_schema.dump(db.session.scalars(db.select(Venue)))


# Read one - /venues/id - GET
@venue_bp.route("/<int:venue_id>")
def get_venue(venue_id):
    # load object data from id
    venue = db.session.scalar(db.select(Venue).filter_by(id=venue_id))
    # check venue exists
    if venue:
        # return requested object data
        return venue_schema.dump(venue)
    else:
        # return error message
        return {"message": f"Venue with id {venue_id} does not exist"}, 404

# Update - /venues/id - PUT, PATCH
@venue_bp.route("/<int:venue_id>", methods=["PUT", "PATCH"])
def update_venue(venue_id):
    # integrity error try/except for unique violations
    try:
        # load object data from id
        venue = db.session.scalar(db.select(Venue).filter_by(id=venue_id))
        # load input data
        body_data = request.get_json()
        # body_data = venue_schema.load(request.get_json(), partial=True)
        # check venue exists
        if venue:
            # assign new values or use old ones
            venue.name = body_data.get("name") or venue.name
            venue.phone = body_data.get("phone") or venue.phone
            # commit changes
            db.session.commit()
            # return new object
            return venue_schema.dump(venue)
        # if no venue
        else:
            # return error message
            return {"message": f"Venue with id {venue_id} does not exist"}, 404
    except IntegrityError:
        # return error message
        return {"message": "Venue phone number already in use"}, 409

# Delete - /venues/id - DELETE
@venue_bp.route("/<int:venue_id>", methods=["DELETE"])
def delete_venue(venue_id):
    # load object data from id
    venue = db.session.scalar(db.select(Venue).filter_by(id=venue_id))
    # check venue exists
    if venue:
        # delete the object
        db.session.delete(venue)
        # commit to session
        db.session.commit()
        # return successful
        return {"message": f"Venue '{venue.name}' deleted successfully"}
    # if no venue
    else:
        # return error message
        return {"message": f"Venue with id {venue_id} does not exist"}, 404