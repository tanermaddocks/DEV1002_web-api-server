from marshmallow import fields

from local_import.init import db, ma

# Model
class Table(db.Model):
    # Table name
    __tablename__ = "tables"
    
    # Columns
    id = db.Column(db.Integer, primary_key=True)
    max_guests = db.Column(db.String, nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey("venues.id"), nullable=False)

    # Relationships
    venue = db.relationship("Venue", back_populates="tables")
    booking_table = db.relationship("Booking_table", back_populates="tables", cascade="all, delete")

# Schema
class TableSchema(ma.Schema):
    # Modifiers
    venue = fields.Nested("VenueSchema", only=["name"])
    # Fields
    class Meta:
        fields = ("id", "max_guests", "venue_id", "venue" ,"booking_tables")

# Schema variables
table_schema = TableSchema()
tables_schema = TableSchema(many=True)