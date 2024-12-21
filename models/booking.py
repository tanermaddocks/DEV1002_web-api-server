from marshmallow import fields

from local_import.init import db, ma

# Model
class Booking(db.Model):
    # Table name
    __tablename__ = "bookings"
    
    # Columns
    booking_id = db.Column(db.Integer, primary_key=True)
    num_guests = db.Column(db.Integer, nullable=False)
    guest_id = db.Column(db.Integer, db.ForeignKey("guests.guest_id"), nullable=False)
    time = db.Column(db.Date, nullable=False)

    # Relationships
    guest = db.relationship("Guest", back_populates="bookings")
    allocations = db.relationship("Allocation", back_populates="booking", cascade="all, delete")

# Schema
class BookingSchema(ma.Schema):
    # Modifiers
    guest = fields.Nested("GuestSchema", only=["name"])
    allocations = fields.List(fields.Nested("AllocationSchema", only=["table_id"]))
    # Fields
    class Meta:
        fields = ("booking_id", "guest_id", "num_guests", "guest" ,"allocations")

# Schema variables 
booking_schema = BookingSchema()
bookings_schema = BookingSchema(many=True)