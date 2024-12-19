from marshmallow import fields

from local_import.init import db, ma

# Model
class Guest(db.Model):
    # Table name
    __tablename__ = "guests"
    
    # Columns
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    phone = db.Column(db.String, nullable=False, unique=True)
    email = db.Column(db.String, unique=True)

    # Relationships
    bookings = db.relationship("Booking", back_populates="guest", cascade="all, delete")

# Schema
class GuestSchema(ma.Schema):
    # Modifiers
    bookings = fields.Nested("BookingSchema", exclude=["guest"])
    # Fields
    class Meta:
        fields = ("id", "name", "phone", "email", "bookings")

# Schema variables
guest_schema = GuestSchema()
guests_schema = GuestSchema(many=True)