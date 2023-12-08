from flask import Blueprint, jsonify, request,current_app
from app import db
from app.models import Student,Course
from sqlalchemy.exc import SQLAlchemyError

course_blueprint = Blueprint('course',__name__)

# api to create a course
@course_blueprint.route('/courses', methods=['POST'])
def create_course():
    data = request.json
    new_course = Course(name=data['name'])
    db.session.add(new_course)
    db.session.commit()
    return jsonify({"course":new_course.serialize(),"message":"course created successfully"}), 201

# api to get all the courses
@course_blueprint.route('/courses', methods=['GET'])
def get_all_courses():
    courses = Course.query.all()
    serialized_courses = [ course.serialize() for course in courses]
    return jsonify({"courses":serialized_courses}), 200

# api to get course by course_id
@course_blueprint.route('/courses/<int:course_id>', methods=['GET'])
def get_course_by_id(course_id):
    course = Course.query.get(course_id)

    if course is None:
        return jsonify({"message": "Course not found"}), 404
    return jsonify({"course": course.serialize()}), 200

# api to  delete course by course_id
@course_blueprint.route('/courses/<int:course_id>', methods=['DELETE'])
def delete_course(course_id):
    course = Course.query.get(course_id)

    if course is None:
        return jsonify({"message": "Course not found"}), 404

    db.session.delete(course)
    db.session.commit()

    return jsonify({"course":course.serialize(), "message": "Course deleted successfully"}), 200

