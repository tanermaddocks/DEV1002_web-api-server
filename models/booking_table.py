from marshmallow import fields

from local_import.init import db, ma

# Model
class BookingTable(db.Model):
    # Table name
    __tablename__ = "bookings_tables"
    
    # Columns
    id = db.Column(db.Integer, primary_key=True)
    booking_id = db.Column(db.Integer, db.ForeignKey("bookings.id"), nullable=False)
    table_id = db.Column(db.Integer, db.ForeignKey("tables.id"), nullable=False)

    # Relationships
    booking = db.relationship("Booking", back_populates="bookings_tables")
    table = db.relationship("Table", back_populates="bookings_tables")

# Schema
class BookingTableSchema(ma.Schema):
    # Modifiers
    booking = fields.Nested("BookingSchema", exclude=["bookings_tables"])
    table = fields.Nested("TableSchema", exclude=["bookings_tables"])
    # Fields
    class Meta:
        fields = ("id", "booking_id", "table_id", "booking", "table")

# Schema variables
booking_table_schema = BookingTableSchema()
bookings_tables_schema = BookingTableSchema(many=True)