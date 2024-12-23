from marshmallow import fields

from local_import.init import db, ma

# Model
class Allocation(db.Model):
    # Table name
    __tablename__ = "allocations"

    # Table arguments
    __table_args__ = (
        db.UniqueConstraint("booking_id", "table_id", name="unique_booking_table"),
    )
    
    # Columns
    allocation_id = db.Column(db.Integer, primary_key=True)
    booking_id = db.Column(db.Integer, db.ForeignKey("bookings.booking_id"), nullable=False)
    table_id = db.Column(db.Integer, db.ForeignKey("tables.table_id"), nullable=False)

    # Relationships
    booking = db.relationship("Booking", back_populates="allocations")
    table = db.relationship("Table", back_populates="allocations")

# Schema
class AllocationSchema(ma.Schema):
    # Modifiers
    booking = fields.Nested("BookingSchema", exclude=["allocations"])
    table = fields.Nested("TableSchema", exclude=["allocations"])
    # Fields
    class Meta:
        fields = ("allocation_id", "booking_id", "table_id", "booking", "table")

# Schema variables
allocation_schema = AllocationSchema()
allocations_schema = AllocationSchema(many=True)