from flask import Blueprint, request
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes

from local_import.init import db
from models.allocation import Allocation, allocations_schema, allocation_schema

allocation_bp = Blueprint("allocations", __name__, url_prefix="/allocations")

# Create - /allocations - POST
@allocation_bp.route("/", methods=["POST"])
def create_allocation():
    # integrity error try/except for not_null violations
    try:
        # get data from body
        body_data = request.get_json()
        # create instances
        new_allocation = Allocation(
            booking_id = body_data.get("booking_id"),
            table_id = body_data.get("table_id")
        )
        # add to session
        db.session.add(new_allocation)
        # commit new object
        db.session.commit()
        # return new object
        return allocation_schema.dump(new_allocation), 201
    except IntegrityError as err:
        # check for error not_null
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            # return error message
            return {"message": f"The field '{err.orig.diag.column_name}' is required"}, 409

# Read all - /allocations - GET
@allocation_bp.route("/")
def get_allocations():
    # return all items in table
    return allocations_schema.dump(db.session.scalars(db.select(Allocation)))


# Read one - /allocations/id - GET
@allocation_bp.route("/<int:allocation_id>")
def get_allocation(allocation_id):
    # load object data from id
    allocation = db.session.scalar(db.select(Allocation).filter_by(id=allocation_id))
    # check allocation exists
    if allocation:
        # return requested object data
        return allocation_schema.dump(allocation)
    else:
        # return error message
        return {"message": f"Allocation with id {allocation_id} does not exist"}, 404

# Update - /allocations/id - PUT, PATCH
@allocation_bp.route("/<int:allocation_id>", methods=["PUT", "PATCH"])
def update_allocation(allocation_id):
    # load object data from id
    allocation = db.session.scalar(db.select(Allocation).filter_by(id=allocation_id))
    # load input data
    body_data = request.get_json()
    # body_data = allocation_schema.load(request.get_json(), partial=True)
    # check allocation exists
    if allocation:
        # assign new values or use old ones
        allocation.booking_id = body_data.get("booking_id") or allocation.name
        allocation.table_id = body_data.get("table_id") or allocation.phone
        # commit changes
        db.session.commit()
        # return new object
        return allocation_schema.dump(allocation)
    # if no allocation
    else:
        # return error message
        return {"message": f"Allocation with id {allocation_id} does not exist"}, 404

# Delete - /allocations/id - DELETE
@allocation_bp.route("/<int:allocation_id>", methods=["DELETE"])
def delete_allocation(allocation_id):
    # load object data from id
    allocation = db.session.scalar(db.select(Allocation).filter_by(id=allocation_id))
    # check allocation exists
    if allocation:
        # delete the object
        db.session.delete(allocation)
        # commit to session
        db.session.commit()
        # return successful
        return {"message": f"Allocation with id {allocation_id} deleted successfully"}
    # if no allocation
    else:
        # return error message
        return {"message": f"Allocation with id {allocation_id} does not exist"}, 404