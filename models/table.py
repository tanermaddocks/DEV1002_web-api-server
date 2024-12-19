from marshmallow import fields

from local_import.init import db, ma

# Model
class Table(db.Model):
    # Table name
    __tablename__ = "tables"
    
    # Columns
    id = db.Column(db.Integer, primary_key=True)
    table_number = db.Column(db.Integer, nullable=False) #add in parameter for table#/venueid
    max_guests = db.Column(db.String, nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey("venues.id"), nullable=False)

    # Relationships
    venue = db.relationship("Venue", back_populates="tables")
    bookings_tables = db.relationship("BookingTable", back_populates="table", cascade="all, delete")

# Schema
class TableSchema(ma.Schema):
    # Modifiers
    venue = fields.Nested("VenueSchema", only=["name"])
    bookings_tables = fields.Nested("BookingTableSchema", exclude=["table"])
    # Fields
    class Meta:
        fields = ("id", "table_number", "max_guests", "venue_id", "venue" ,"bookings_tables")

# Schema variables
table_schema = TableSchema()
tables_schema = TableSchema(many=True)