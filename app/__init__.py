from flask import Flask, jsonify, request, current_app
from flask_sqlalchemy import SQLAlchemy
from config import Config
from sqlalchemy.exc import SQLAlchemyError
import jwt


db = SQLAlchemy()

def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)

    with app.app_context():
        from .models import User, Student
        db.create_all()
   
    #    import the blueprints
    from app.views.auth import auth_blueprint
    from app.views.students import students_blueprint
    from app.views.course import course_blueprint
    from app.views.enroll import enroll_blueprint


    # register blueprints
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(students_blueprint)
    app.register_blueprint(course_blueprint)
    app.register_blueprint(enroll_blueprint)


    @app.before_request
    def authenticate():
        # skip authentication for excuded endpoints
        excluded_endpoints = ['auth.login','auth.register']
        if request.endpoint in excluded_endpoints:
            return

        jwt_token = request.headers.get('Authorization')
        if jwt_token is None or len(jwt_token) ==  0:
            return jsonify({"message": "token mission in authorization header"}), 401

        if jwt_token is not None:
            try:
                try:
                    jwt_token = jwt_token.split(' ')[1]
                except:
                    return jsonify({"message": "Invalid token"}), 401
  
                decoded_token = jwt.decode(jwt_token, current_app.config['JWT_SECRET_KEY'], algorithms=['HS256'])
                current_user = decoded_token.get('username')
                setattr(request, 'current_user', current_user)
            except jwt.ExpiredSignatureError:
                return jsonify({"message": "Token has expired"}), 401
            except jwt.InvalidTokenError:
                return jsonify({"message": "Invalid token"}), 401

    return app
