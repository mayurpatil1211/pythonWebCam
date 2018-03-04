# learnwiz/auth_user/controller.py


from flask import Blueprint, jsonify, request
from sqlalchemy import exc, or_
import jwt
from jwt import decode, encode
from app.mod_auth.utils import authenticate
from app.mod_auth.models import *
from app import db, bcrypt


auth_blueprint = Blueprint('auth', __name__)


@auth_blueprint.route('/auth/register', methods=['POST'])
def register_user():
    # get post data
    post_data = request.get_json()
    if not post_data:
        response_object = {
            'status': 'error',
            'message': 'Invalid payload.'
        }
        return jsonify(response_object), 400
    #get data from Json
    first_name = post_data.get('first_name')
    last_name = post_data.get('last_name')
    email = post_data.get('email')
    role = post_data.get('usr_role')
    classes = post_data.get('classes')

    #set Default Password
    password = 'learnwiz123'

    role_id = User_roles.query.filter_by(id=role).first()
    try:
        # check for existing user
        user = User.query.filter(
            or_(User.email==email)).first()
        if not user:
            # add new user to db
            new_user = User(
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=password,
                user_roles_id=role_id.id,
            )
            db.session.add(new_user)
            print(type(role_id.id))

            #check whether Teacher Or Student Or Admin
            if role_id.id==2 or role_id.id==3:
                if not classes:
                    print("classes are not there")
                    response_object = {
                        'status': 'error',
                        'message': 'Something Went Wrong. Please Check Your Information'
                    }
                    return jsonify(response_object), 400
                elif len(classes)>0:
                    for i in classes:
                        class_details = Classes.query.filter_by(id=i).first()
                        new_user.class_users.append(class_details)
                        db.session.add(new_user)

                    db.session.commit()
                    response_object = {
                        'status': 'success',
                        'message': 'Successfully registered.'
                    }
                    return jsonify(response_object), 201
                else:
                    response_object = {
                        'status': 'error',
                        'message': 'Something Went Wrong. Please Check Your Information'
                    }
                    return jsonify(response_object), 400
            else:
                db.session.commit()
                response_object = {
                    'status': 'success',
                    'message': 'Successfully registered.'
                }
                return jsonify(response_object), 201
        else:
            response_object = {
                'status': 'error',
                'message': 'Sorry. That user already exists.'
            }
            return jsonify(response_object), 400
    # handler errors
    except (exc.IntegrityError, ValueError) as e:
        db.session().rollback()
        response_object = {
            'status': 'error',
            'message': 'Invalid payload.'
        }
        return jsonify(response_object), 400



@auth_blueprint.route('/users', methods=['GET'])
@authenticate
def list_user(res):
    peter = User.query.filter_by(email='mayur11@gmail.com').first()
    response_object = {
        'status': 'success',
        'user': peter.email,
        'pwd': peter.password
    }
    return jsonify(response_object), 200
   



@auth_blueprint.route('/auth/login', methods=['POST'])
def login_user():
    # get post data
    post_data = request.get_json()
    if not post_data:
        response_object = {
            'status': 'error',
            'message': 'Invalid payload.'
        }
        return jsonify(response_object), 400
    email = post_data.get('usr_email')
    password = post_data.get('usr_password')
    try:
        # fetch the user data
        user = User.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password, password):
            auth_token = user.encode_auth_token(user.id)
            user_role = user.user_roles_id
            isActive = User_roles.query.filter_by(id=user_role).first()
            print (isActive.status)
            if auth_token and (isActive.status=='Active'):
                response_object = {
                    'status': 'success',
                    'user_id': user.id,
                    'username': user.first_name,
                    'message': 'Successfully logged in.',
                    'user_role': user.user_roles_id, 
                    'auth_token': auth_token.decode()
                }
                return jsonify(response_object), 200
            else:
                response_object = {
                'status': 'error',
                'message': 'Your Account is Inactive, please contact to the Administrator'
                }
                return jsonify(response_object), 400
        else:
            response_object = {
                'status': 'error',
                'message': 'User does not exist.'
            }
            return jsonify(response_object), 400
    except Exception as e:
        print(e)
        response_object = {
            'status': 'error',
            'message': 'Try again.'
        }
        return jsonify(response_object), 500





@auth_blueprint.route('/auth/logout', methods=['GET'])
@authenticate
def logout_user(resp):
    response_object = {
        'status': 'success',
        'message': 'Successfully logged out.'
    }
    return jsonify(response_object), 200





@auth_blueprint.route('/auth/status', methods=['GET'])
@authenticate
def get_user_status(resp):
    user = User.query.filter_by(id=resp).first()
    response_object = {
        'status': 'success',
        'data': {
            'id': user.id,
            'email': user.email,
            'active': user.active,
            'created_at': user.created_at
        }
    }
    return jsonify(response_object), 200




@auth_blueprint.route('/users/teacher', methods=['GET'])
def teacher_list():
    selectedTeachers = []
    # selectedTeachers = {}

    teachers = User.query.filter_by(user_roles_id=2).all()

    if len(teachers)<0:
        response_object = {
            'status': 'error',
            'message': 'Invalid payload.'
        }
        return jsonify(response_object), 400
    elif len(teachers)>0:
        for a in teachers:
            teacher = {
            'teacher_id': a.id,
            'teacher_first_name': a.first_name,
            'teacher_last_name': a.last_name,
            'teacher_email': a.email,
            'teacher_is_active': a.active,
            'teacher_created': a.created_at
            }
            selectedTeachers.append(teacher)
    return jsonify(selectedTeachers), 200


@auth_blueprint.route('/users/student', methods=['GET'])
def student_list():
    selectedStudents = []
    # selectedTeachers = {}

    students = User.query.filter_by(user_roles_id=3).all()

    if len(students)<0:
        response_object = {
            'status': 'error',
            'message': 'Invalid payload.'
        }
        return jsonify(response_object), 400
    elif len(students)>0:
        for a in students:
            student = {
            'student_id': a.id,
            'student_first_name': a.first_name,
            'student_last_name': a.last_name,
            'student_email': a.email,
            'student_is_active': a.active,
            'student_created': a.created_at
            }
            selectedStudents.append(student)
    return jsonify(selectedStudents), 200

