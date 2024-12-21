import os

from flask import Flask

from local_import.init import db, ma
from local_import.controllers import *

def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URI")

    db.init_app(app)
    ma.init_app(app)

    # @app.errorhandler(ValidationError)
    # def validation_error(err):
    #     return {"message": err.messages}, 400
    
    # @app.errorhandler(400)
    # def bad_request(err):
    #     return {"message": str(err)}, 400
    
    # @app.errorhandler(404)
    # def not_found(err):
    #     return {"message": str(err)}, 404
    
    app.register_blueprint(db_commands)
    app.register_blueprint(venue_bp)
    app.register_blueprint(guest_bp)
    app.register_blueprint(table_bp)
    app.register_blueprint(booking_bp)
    app.register_blueprint(allocation_bp)

    return app