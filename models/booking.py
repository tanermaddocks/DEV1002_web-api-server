from marshmallow import fields

from local_import.init import db, ma

# Model
class Booking(db.Model):
    # Booking name
    __bookingname__ = "bookings"
    
    # Columns
    id = db.Column(db.Integer, primary_key=True)
    max_guests = db.Column(db.String, nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey("venues.id"), nullable=False, unique=True)

    # Relationships
    guest = db.relationship("Guest", back_populates="bookings")
    booking_table = db.relationship("BookingTable", back_populates="booking", cascade="all, delete")

# Schema
class BookingSchema(ma.Schema):
    # Modifiers
    venue = fields.Nested("VenueSchema", only=["name"])
    # Fields
    class Meta:
        fields = ("id", "max_guests", "venue_id", "guest" ,"booking_table")

# Schema variables
booking_schema = BookingSchema()
bookings_schema = BookingSchema(many=True)