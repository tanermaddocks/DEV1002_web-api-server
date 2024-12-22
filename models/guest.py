from marshmallow import fields
from marshmallow.validate import Regexp, And, Length

from local_import.init import db, ma

# Model
class Guest(db.Model):
    # Table name
    __tablename__ = "guests"
    
    # Columns
    guest_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    phone = db.Column(db.String, nullable=False, unique=True)
    email = db.Column(db.String, unique=True)

    # Relationships
    bookings = db.relationship("Booking", back_populates="guest", cascade="all, delete")

# Schema
class GuestSchema(ma.Schema):
    # Validations
    name = fields.String(validate=And(
        Length(min=2, error="Name must be at least 2 characters long"),
        Regexp('^[A-Za-z][A-Za-z0-9 ]*$',
               error="Only letters, numbers and spaces are allowed")
               ))
    phone = fields.String(
        validate=Regexp("(?:\+?61)?(?:\(0\)[23478]|\(?0?[23478]\)?)\d{8}",
                        error="Input a valid Australian phone number"
                        ))
    email = fields.String(
        validate=Regexp("^[\w-\.]+@([\w-]+\.)+[\w-]{2,4}$",
                        error="Input a valid email address"
                        ))
    # Modifiers
    bookings = fields.Nested("BookingSchema", exclude=["guest"])
    # Fields
    class Meta:
        fields = ("guest_id", "name", "phone", "email", "bookings")

# Schema variables
guest_schema = GuestSchema()
guests_schema = GuestSchema(many=True)