from flask import Blueprint, jsonify, request,current_app
from app import db
from app.models import Student,Course,Enrollment
from sqlalchemy.exc import SQLAlchemyError

enroll_blueprint = Blueprint('enroll',__name__)

@enroll_blueprint.route('/enrollments', methods=['POST'])
def enroll_student_in_course():
    data = request.json
    student_id = data.get('student_id')
    course_id = data.get('course_id')

    if not student_id or not course_id:
        return jsonify({"message":"student_id and course_id are required"}),400

    student = Student.query.get(student_id)
    course = Course.query.get(course_id)

    if student is None:
        return jsonify({"message": "Student not found with the given student_id"}),404
    if course is None:
        return jsonify({"message":"Course not found with the given course_id"}),404


    # check if the student is already enrolled
    existing_enrollment = Enrollment.query.filter_by(student_id=student_id, course_id=course_id).first()

    if existing_enrollment:
        return jsonify({"message":"student is already enrolled in the course"})

    # create a new enrollment
    new_enrollment = Enrollment(student_id=student_id, course_id=course_id)
    db.session.add(new_enrollment)
    db.session.commit()

    return jsonify({"message":"Student enrolled in the course successfully"}), 201


