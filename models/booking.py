from marshmallow import fields

from local_import.init import db, ma

# Model
class Booking(db.Model):
    # Booking name
    __bookingname__ = "bookings"
    
    # Columns
    id = db.Column(db.Integer, primary_key=True)
    num_guests = db.Column(db.Integer, nullable=False)
    guestId = db.Column(db.Integer, db.ForeignKey("guest.id"), nullable=False)
    time = db.Column(db.Date, nullable=False)

    # Relationships
    guest = db.relationship("Guest", back_populates="bookings")
    booking_table = db.relationship("BookingTable", back_populates="booking", cascade="all, delete")

# Schema
class BookingSchema(ma.Schema):
    # Modifiers
    venue = fields.Nested("VenueSchema", only=["name"])
    # Fields
    class Meta:
        fields = ("id", "guest_id", "num_guests", "guest" ,"booking_table")

# Schema variables 
booking_schema = BookingSchema()
bookings_schema = BookingSchema(many=True)