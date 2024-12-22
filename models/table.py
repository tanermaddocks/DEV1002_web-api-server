from marshmallow import fields, validates
from marshmallow.exceptions import ValidationError

from local_import.init import db, ma

# Model
class Table(db.Model):
    # Table name
    __tablename__ = "tables"

    # Table arguments
    __table_args__ = (
        db.UniqueConstraint("venue_id", "table_number", name="unique_venue_table_number")
    )
    
    # Columns
    table_id = db.Column(db.Integer, primary_key=True)
    table_number = db.Column(db.Integer, nullable=False) #add in parameter for table#/venueid
    max_guests = db.Column(db.Integer, nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey("venues.venue_id"), nullable=False)

    # Relationships
    venue = db.relationship("Venue", back_populates="tables")
    allocations = db.relationship("Allocation", back_populates="table", cascade="all, delete")

# Schema
class TableSchema(ma.Schema):
    # Validations
    @validates("max_guests")
    def validate_max_guests(self, value):
        if value < 1:
            raise ValidationError("A table must sit at least one person")
    # Modifiers
    venue = fields.Nested("VenueSchema", only=["venue_id", "name"])
    allocations = fields.List(fields.Nested("AllocationSchema", only=["booking_id"]))
    # Fields
    class Meta:
        fields = ("table_id", "table_number", "max_guests", "venue" ,"allocations")

# Schema variables
table_schema = TableSchema()
tables_schema = TableSchema(many=True)