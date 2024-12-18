from marshmallow import fields

from local_import.init import db, ma

# Model
class Booking(db.Model):
    # Table name
    __tablename__ = "bookings"
    
    # Columns
    id = db.Column(db.Integer, primary_key=True)
    num_guests = db.Column(db.Integer, nullable=False)
    guest_id = db.Column(db.Integer, db.ForeignKey("guests.id"), nullable=False)
    time = db.Column(db.Date, nullable=False)

    # Relationships
    guest = db.relationship("Guest", back_populates="bookings")
    bookings_tables = db.relationship("BookingTable", back_populates="booking", cascade="all, delete")

# Schema
class BookingSchema(ma.Schema):
    # Modifiers
    guest = fields.Nested("GuestSchema", only=["name"])
    bookings_tables = fields.List(fields.Nested("BookingTableSchema", only=["booking_id"]))
    # Fields
    class Meta:
        fields = ("id", "guest_id", "num_guests", "guest" ,"bookings_tables")

# Schema variables 
booking_schema = BookingSchema()
bookings_schema = BookingSchema(many=True)