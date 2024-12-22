from datetime import date

from marshmallow import fields, validates
from marshmallow.exceptions import ValidationError

from local_import.init import db, ma

# Model
class Booking(db.Model):
    # Table name
    __tablename__ = "bookings"
    
    # Columns
    booking_id = db.Column(db.Integer, primary_key=True)
    num_guests = db.Column(db.Integer, nullable=False)
    guest_id = db.Column(db.Integer, db.ForeignKey("guests.guest_id"), nullable=False)
    booking_date = db.Column(db.Date, nullable=False)

    # Relationships
    guest = db.relationship("Guest", back_populates="bookings")
    allocations = db.relationship("Allocation", back_populates="booking", cascade="all, delete")

# Schema
class BookingSchema(ma.Schema):
    # Validations
    @validates("max_guests")
    def validate_max_guests(self, value):
        if value < 1:
            raise ValidationError("A booking must include at least one person")
        
    @validates('booking_date')
    def validate_enrolment_date(self, value):
        today = date.today()
        if date.fromisoformat(value) < today:
            raise ValidationError("Booking date cannot be before today")

    # Modifiers
    guest = fields.Nested("GuestSchema", only=["name"])
    allocations = fields.List(fields.Nested("AllocationSchema", only=["table_id"]))

    # Fields
    class Meta:
        fields = ("booking_id", "guest_id", "booking_date", "num_guests", "guest" ,"allocations")

# Schema variables 
booking_schema = BookingSchema()
bookings_schema = BookingSchema(many=True)