from marshmallow import fields

from init import db, ma

class Venue(db.Model):
    __tablename__ = "venues"
    
    # Columns
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    phone = db.Column(db.String, nullable=False, unique=True)

    # Relationships
    tables = db.relationship("Table", back_populates="restaurant", cascade="all, delete")

class VenueSchema(ma.Schema):

    tables = fields.Nested("TablesSchema", exclude=["venue"])

    class Meta:
        fields = ("id", "name", "phone", "tables")

venue_schema = VenueSchema()
venues_schema = VenueSchema(many=True)