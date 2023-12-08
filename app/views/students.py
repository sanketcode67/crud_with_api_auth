from flask import Blueprint, jsonify, request,current_app
from app import db
from app.models import Student,Enrollment,Course
from sqlalchemy.exc import SQLAlchemyError

students_blueprint = Blueprint('students', __name__)





# api to get all the students
@students_blueprint.route('/students', methods=['GET'])
def get_students():
    current_user = getattr(request, 'current_user', None)

    if current_user is None:
        return jsonify({"message": "User not authenticated"}), 401

    try:
        students = Student.query.all()
        serialized_students = [student.serialize() for student in students]
        return jsonify({"username": current_user, "students": serialized_students}), 200
    except SQLAlchemyError as e:
        return jsonify({"message": f"Database error: {str(e)}"}), 500
    

# api to get a student by ID
@students_blueprint.route('/students/<int:student_id>', methods=['GET'])
def get_student_by_id(student_id):
    current_user = getattr(request, 'current_user', None)

    if current_user is None:
        return jsonify({"message": "User not authenticated"}), 401

    try:

        student = Student.query.get(student_id)

        if student is None:
            return jsonify({"message": "Student not found"}), 404

        serialized_student = student.serialize()
        return jsonify({"username": current_user, "student": serialized_student}), 200

    except SQLAlchemyError as e:
        return jsonify({"message": f"Database error: {str(e)}"}), 500


# api to add a student
@students_blueprint.route('/students', methods=['POST'])
def add_student():
    data = request.json

    # Validate age is a valid integer
    try:
        age = int(data['age'])
    except ValueError:
        return jsonify({"error": "Invalid 'age' value. It must be a valid integer."}), 400

    # Check if age is within the specified range
    if not (5 <= age <= 100):
        return jsonify({"error": "Invalid 'age' value. It must be between 5 and 100."}), 400

    new_student = Student(name=data['name'], age=age)

    db.session.add(new_student)
    db.session.commit()

    return jsonify({"message":"student added successfully","student":new_student.serialize()}), 201


# api to delete a student by student_id
@students_blueprint.route('/students/<int:student_id>', methods=['DELETE'])
def delete_student(student_id):
    student = Student.query.get(student_id)

    if student is None:
        return jsonify({"message": "Student not found"}), 404

    db.session.delete(student)
    db.session.commit()
    return jsonify({"message": "Student deleted successfully", "data":student.serialize()})


# api to get all the course details for a given student_id
@students_blueprint.route('/students/<int:student_id>/courses', methods=["GET"])
def get_courses_for_student(student_id):
    student = Student.query.get(student_id)

    if student is None:
        return jsonify({"message":"Student not found"}),404
        
    enrollments = (
        db.session.query(Enrollment, Course)
        .join(Course)
        .filter(Enrollment.student_id == student_id)
        .all()
    )

    if not enrollments:
        return jsonify({"student_id":student_id,"message":"Student is not enrolled in any course"}), 200

    course_details = []

    for enrollment,course in enrollments:
        if course:
            course_details.append(course.serialize().get("name"))     

    return jsonify({"student_id":student_id, "courses":course_details}),200        




