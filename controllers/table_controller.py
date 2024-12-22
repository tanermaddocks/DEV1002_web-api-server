from flask import Blueprint, request
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes

from local_import.init import db
from models.table import Table, tables_schema, table_schema

table_bp = Blueprint("tables", __name__, url_prefix="/tables")

# Create - /tables - POST
@table_bp.route("/", methods=["POST"])
def create_table():
    # integrity error try/except for unique and not_null violations
    try:
        # get data from body
        body_data = table_schema.load(request.get_json(), partial=True)
        # create instance
        new_table = Table(
            max_guests = body_data.get("max_guests"),
            venue_id = body_data.get("venue_id"),
            table_number = body_data.get("table_number")
        )
        # add to session
        db.session.add(new_table)
        # commit new object
        db.session.commit()
        # return new object
        return table_schema.dump(new_table), 201
    except IntegrityError as err:
        # check for error not_null
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            # return error message
            return {"message": f"The field '{err.orig.diag.column_name}' is required"}, 409
        # check for error unique
        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
            # return error message
            return {"message": f"Table number already used in that venue"}, 409


# Read all - /tables - GET
@table_bp.route("/")
def get_tables():
    # return all items in table
    return tables_schema.dump(db.session.scalars(db.select(Table)))


# Read one - /tables/id - GET
@table_bp.route("/<int:table_id>/")
def get_table(table_id):
    # load object data from id
    table = db.session.scalar(db.select(Table).filter_by(table_id=table_id))
    # check table exists
    if table:
        # return requested object data
        return table_schema.dump(table)
    else:
        # return error message
        return {"message": f"Table with id {table_id} does not exist"}, 404

# Update - /tables/id - PUT, PATCH
@table_bp.route("/<int:table_id>/", methods=["PUT", "PATCH"])
def update_table(table_id):
    try:
        # load object data from id
        table = db.session.scalar(db.select(Table).filter_by(table_id=table_id))
        # load input data
        body_data = table_schema.load(request.get_json(), partial=True)
        # check table exists
        if table:
            # assign new values or use old ones
            table.max_guests = body_data.get("max_guests") or table.max_guests
            table.venue_id = body_data.get("venue_id") or table.venue_id
            table.table_number = body_data.get("table_number") or table.table_number
            # commit changes
            db.session.commit()
            # return new object
            return table_schema.dump(table)
        # if no table
        else:
            # return error message
            return {"message": f"Table with id {table_id} does not exist"}, 404
    except IntegrityError as err:
        # check for error unique
        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
            # return error message
            return {"message": f"Table number {table.table_number} already"
                    "used in venue with id {table.venue_id}"}, 409

# Delete - /tables/id - DELETE
@table_bp.route("/<int:table_id>/", methods=["DELETE"])
def delete_table(table_id):
    # load object data from id
    table = db.session.scalar(db.select(Table).filter_by(table_id=table_id))
    # check table exists
    if table:
        # delete the object
        db.session.delete(table)
        # commit to session
        db.session.commit()
        # return successful
        return {"message": f"Table with id {table.id} deleted successfully"}
    # if no table
    else:
        # return error message
        return {"message": f"Table with id {table_id} does not exist"}, 404