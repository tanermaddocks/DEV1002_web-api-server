from marshmallow import fields

from local_import.init import db, ma

# Model
class Table(db.Model):
    # Table name
    __tablename__ = "tables"
    
    # Columns
    table_id = db.Column(db.Integer, primary_key=True)
    table_number = db.Column(db.Integer, nullable=False) #add in parameter for table#/venueid
    max_guests = db.Column(db.Integer, nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey("venues.id"), nullable=False)

    # Relationships
    venue = db.relationship("Venue", back_populates="tables")
    allocations = db.relationship("Allocation", back_populates="table", cascade="all, delete")

# Schema
class TableSchema(ma.Schema):
    # Modifiers
    venue = fields.Nested("VenueSchema", only=["name"])
    allocations = fields.List(fields.Nested("AllocationSchema", only=["booking_id"]))
    # Fields
    class Meta:
        fields = ("table_id", "table_number", "max_guests", "venue_id", "venue" ,"allocations")

# Schema variables
table_schema = TableSchema()
tables_schema = TableSchema(many=True)