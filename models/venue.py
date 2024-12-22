from marshmallow import fields
from marshmallow.validate import Regexp, And, Length

from local_import.init import db, ma

# Model
class Venue(db.Model):
    # Table name
    __tablename__ = "venues"
    
    # Columns
    venue_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    phone = db.Column(db.String, nullable=False, unique=True)

    # Relationships
    tables = db.relationship("Table", back_populates="venue", cascade="all, delete")

# Schema
class VenueSchema(ma.Schema):
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
    # Modifiers
    tables = fields.Nested("TablesSchema", exclude=["venue"])
    # Fields
    class Meta:
        fields = ("venue_id", "name", "phone", "tables")

# Schema variables
venue_schema = VenueSchema()
venues_schema = VenueSchema(many=True)