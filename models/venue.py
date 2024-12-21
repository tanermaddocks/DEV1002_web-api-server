from marshmallow import fields

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
    # Modifiers
    tables = fields.Nested("TablesSchema", exclude=["venue"])
    # Fields
    class Meta:
        fields = ("venue_id", "name", "phone", "tables")

# Schema variables
venue_schema = VenueSchema()
venues_schema = VenueSchema(many=True)