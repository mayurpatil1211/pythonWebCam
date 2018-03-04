from flask import Blueprint, jsonify, request
from sqlalchemy import exc, or_
from sqlalchemy import update
#Import from auth module
from app.mod_auth.utils import authenticate
from app.mod_auth.models import *

#import from class_subject
from app.class_subject.models import *
from app.slides.models import *
from app.homework.models import *

from app import db, bcrypt


class_blueprint = Blueprint('class', __name__)




@class_blueprint.route('/api/add_class', methods=['POST'])
def add_class():
    post_data = request.get_json()
    if not post_data:
        response_object = {
            'status': 'error',
            'message': 'Invalid payload'
        }
        return jsonify(response_object), 400
    class_name = post_data.get('class_name')
    assign_subjects = post_data.get('subjects')
    try:
        new_class = Classes(
            class_name=class_name
            )
        db.session.add(new_class)
        if len(assign_subjects)>0:
            for subject in assign_subjects:
                sub_id = Subjects.query.filter_by(id=subject).first()
                new_class.class_subjects.append(sub_id)
                db.session.add(new_class)
            db.session.commit()
            response_object = {
            'status': 'success',
            'message': 'Class Added Successfully'
            }
            return jsonify(response_object), 201
        else:
            response_object = {
            'status': 'error',
            'message': 'Something Went wrong'
            }
            return jsonify(response_object), 400
    except (exc.IntegrityError, ValueError) as e:
        db.session().rollback()
        response_object = {
            'status' : 'error',
            'message': 'Invalid payload.'
        }
        return jsonify(response_object),400



@class_blueprint.route('/api/add_subject', methods=['POST'])
def add_subject():
    post_data = request.get_json()
    if not post_data:
        response_object={
            'status': 'error',
            'message': 'Invalid payload.'
        }
        return jsonify(response_object), 400
    subject_name = post_data.get('subject_name')
    try:
        new_subject = Subjects(
                subject_name = subject_name
            )
        db.session.add(new_subject)
        db.session.commit()
        response_object={
            'status': 'success',
            'message': 'subject added successfully'
        }
        return jsonify(response_object), 201
    except (exc.IntegrityError, ValueError) as e:
        db.session().rollback()
        response_object = {
            'status': 'error',
            'message': 'Invalid payload.'
        }
        return jsonify(response_object), 400


@class_blueprint.route('/api/add_module', methods=['POST'])
def add_module():
    post_data = request.get_json()
    if not post_data:
        response_object = {
            'status':'error',
            'message':'Invalid payload'
        }
        return jsonify(response_object), 400
    module_name = post_data.get('module_name')
    subject_id = post_data.get('subject_id')
    class_id = post_data.get('class_id')
    url = None
    try:
        classes = Classes.query.filter_by(id = class_id).first()
        subject = Subjects.query.filter_by(id = subject_id).first()

        if not classes and subject:
            response_object={
                'status': 'error',
                'message': 'Bad request'
            }
            return jsonify(response_object), 400
        elif classes and subject:
            new_module = Modules(
                module_name = module_name,
                url = url,
                class_id = classes.id,
                subject_id = subject.id
                )
            db.session.add(new_module)
            db.session.commit()
            response_object = {
                'status': 'success',
                'message': 'Module added successfully'
            }
            return jsonify(response_object),201
    except (exc.IntegrityError, ValueError) as e:
        db.session().rollback()
        response_object = {
        'status': 'error',
        'message' : 'Invalid payload'
        }
        return jsonify(response_object), 400


# @class_blueprint.route('/api/view_subjects', methods=['POST'])
# def view_subjects():
#   post_data = request.get_json()
#   if not post_data:
#       response_object = {
#           'status': 'error',
#           'message': 'Invalid payload'
#       }
#       return jsonify(response_object), 400

#   id_class = post_data.get('class_id')
#   user_id = post_data.get('user_id')
#   try:
#       subject_list=[]
#       user = User.query.filter_by(id = user_id).first()
#       if user is not None:
#           query_user_class = Classes.query.join(class_user_table).join(User).filter(class_user_table.c.user_id == user.id and class_user_table.c.class_id == id_class).first()
#           # print (query_user_class.id)
#           if query_user_class is not None:
#               query_class_subject = Subjects.query.join(class_subject_table).join(Classes).filter(class_subject_table.c.class_id == id_class).all()
#               print(len(query_class_subject))
#               for sub in query_class_subject:
#                   subject = {
#                       'subject_id': sub.id,
#                       'subject_name': sub.subject_name
#                   }
#                   subject_list.append(subject)
#               return jsonify({'status': 'success','subject_list':subject_list}), 200
#           else:
#               response_object = {
#                   'status':'error',
#                   'message': 'Something Went Wrong. Please check Request or Contact to the Support'
#               }
#               return jsonify(response_object), 400
#       else:
#           response_object = {
#               'status': 'error',
#               'message' : 'Invalid User'
#           }
#           return jsonify(response_object), 400

#   except (exc.IntegrityError, ValueError) as e:
#       response_object = {
#           'status': 'error',
#           'message': 'Invalid payload'
#       }
#       return jsonify(response_object), 400


@class_blueprint.route('/api/subjects/<user_id>/<class_id>', methods=['GET'])
def list_subjectModules(user_id, class_id):
    subject_list = []
    try:
        user = User.query.filter_by(id = user_id).first()
        if user is not None:
            query_user_class = Classes.query.join(class_user_table).join(User).filter(class_user_table.c.user_id == user.id and class_user_table.c.class_id == id_class).first()
            if query_user_class is not None:
                query_class_subject = Subjects.query.join(class_subject_table).join(Classes).filter(class_subject_table.c.class_id == class_id).all()
                for sub in query_class_subject:
                    subject={}
                    subject['id'] = sub.id
                    subject['name'] = sub.subject_name

                    modules = Modules.query.filter_by(subject_id=sub.id, class_id=class_id).all()
                    subject['module'] = []
                    for j in modules:
                        module = {
                            'mid': j.id,
                            'mname': j.module_name
                        }
                        subject['module'].append(module)
                    subject_list.append(subject)
                return jsonify({'status':'success', 'subjects_list': subject_list}),200
            else:
                response_object={
                    'status':'error',
                    'message': 'Inavalid User or Class Id'
                }
                return jsonify(response_object), 400
        else:
            response_object={
                'status': 'error',
                'message': 'Invalid User'
            }
            return jsonify(response_object), 400
    except (exc.IntegrityError, ValueError) as e:
        response_object = {
            'status':'error',
            'message':'Inavalid payload'
        }
        return jsonify(response_object), 400




@class_blueprint.route('/api/classess/<user_id>', methods=['GET'])
def list_classes(user_id):
    class_list=[]
    try:
        user = User.query.filter_by(id = user_id).first()
        if user is not None:
            query_user_class = Classes.query.join(class_user_table).join(User).filter(class_user_table.c.user_id == user.id).all()
            if query_user_class is not None:
                for item in query_user_class:
                    classes = {}
                    classes['id'] = item.id
                    classes['name'] = item.class_name

                    query_class_subject = Subjects.query.join(class_subject_table).join(Classes).filter(class_subject_table.c.class_id == item.id).all()
                    classes['subject_list'] = []
                    for sub in query_class_subject:
                        
                        subject={}
                        subject['id'] = sub.id
                        subject['name'] = sub.subject_name

                        modules = Modules.query.filter_by(subject_id=sub.id, class_id=item.id).all()
                        subject['module'] = []
                        for j in modules:
                            module = {
                                'mid': j.id,
                                'mname': j.module_name
                            }
                            subject['module'].append(module)
                        classes['subject_list'].append(subject)
                    class_list.append(classes)
                return jsonify({'status':'success', 'classes_list': class_list}),200
            else:
                response_object={
                    'status':'error',
                    'message': 'Inavalid User or Class Id'
                }
                return jsonify(response_object), 400
        else:
            response_object={
                'status': 'error',
                'message': 'Invalid User'
            }
            return jsonify(response_object), 400
    except (exc.IntegrityError, ValueError) as e:
        response_object = {
            'status':'error',
            'message':'Inavalid payload'
        }
        return jsonify(response_object), 400




# @class_blueprint.route('/api/view_chapters/<module_id>', methods=['GET'])
# def list_chapters(module_id):
#   chapter_list = []
#   try:
#       chapter_data = Chapters.query.filter_by(module_id=module_id).all()
#       print(chapter_data[0].chapter_name)
        
#       for i in chapter_data:
#           chapter = {}
#           chapter['id'] = i.id
#           chapter['name'] = i.chapter_name
#           chapter['selectDate'] = i.select_date
#           chapter['published'] = i.published
#           chapter['isCompleted'] = i.completed

#           sub_chapters = Subchapters.query.filter_by(chapter_id= i.id).all()
#           chapter['subChapter']=[]
#           for j in sub_chapters:
#               items={
#                   'id': j.id,
#                   'name': j.name,
#                   'selectDate': j.select_date,
#                   'published': j.published,
#                   'isCompleted': j.completed
#               }
#               chapter['subChapter'].append(items)
#           chapter_list.append(chapter)
#       return jsonify({'status': 'success', 'chapters': chapter_list}),200
#   except(exc.IntegrityError, ValueError) as e:
#       response_object = {
#           'status': 'error',
#           'message' : 'Invalid payload'
#       }
#       return jsonify(response_object), 400




# @class_blueprint.route('/api/view_modules/<class_id>/<subject_id>', methods=['GET'])
# def list_modules(class_id, subject_id):
#   modules = []
#   try:
#       module_data = Modules.query.filter_by(class_id = class_id, subject_id=subject_id).all()
#       if module_data is not None:
#           for x in module_data:
#               module = {
#                   "mId" : x.id,
#                   "mName" : x.module_name,
#               }
#               modules.append(module)
#           return jsonify({'status':'success', 'modules_list': modules}), 200
#       else:
#           response_object = {
#               'status': 'error',
#               'message': 'Something went wrong please try again letter or check data'
#           }
#           return jsonify('error'), 400
#   except(exc.IntegrityError, ValueError) as e:
#       response_object = {
#           'status': 'error',
#           'message' : 'Invalid payload'
#       }
#       return jsonify(response_object), 400







@class_blueprint.route('/api/add_chapter', methods=['POST'])
def add_chapter():
    post_data = request.get_json()
    if not post_data:
        response_object={
            'status': 'error',
            'message': 'Invalid payload'
            }
        return jsonify(response_object), 400
    chapter_name = post_data.get('chapter_name')
    url = post_data.get('url')
    select_date = post_data.get('select_date')
    module_id = post_data.get('module_id')

    try:
        module = Modules.query.filter_by(id = module_id).first()
        if module is not None:
            new_chapter = Chapters(
                    chapter_name = chapter_name,
                    url = url,
                    select_date = select_date,
                    module_id = module_id
                )
            db.session.add(new_chapter)
            db.session.commit()
            response_object = {
                'status': 'success',
                'message' : 'Chapter Added Successfully to the Module'
                }
            return jsonify(response_object), 201
        else:
            response_object={
                'status': 'error',
                'message': 'Something went wrong please try again letter or check data'
            }
            return jsonify(response_object), 400
    except(exc.IntegrityError, ValueError) as e:
        response_object = {
            'status': 'error',
            'message' : 'Invalid payload'
            }
        return jsonify(response_object), 400


@class_blueprint.route('/api/add_subchapter', methods=['POST'])
def add_subChapter():
    post_data = request.get_json()
    if not post_data:
        response_object={
            'status': 'error',
            'message': 'Invalid payload'
            }
        return jsonify(response_object), 400
    subchapter_name = post_data.get('name')
    url = post_data.get('url')
    select_date = post_data.get('select_date')
    chapter_id = post_data.get('chapter_id')

    try:
        chapter = Chapters.query.filter_by(id = chapter_id).first()
        if chapter is not None:
            new_subchapter = Subchapters(
                    name = subchapter_name,
                    url = url,
                    select_date = select_date,
                    chapter_id = chapter_id
                )
            db.session.add(new_subchapter)
            db.session.commit()
            response_object = {
                'status': 'success',
                'message' : 'Chapter Added Successfully to the Module'
                }
            return jsonify(response_object), 201
        else:
            response_object={
                'status': 'error',
                'message': 'Something went wrong please try again letter or check data'
                }
            return jsonify(response_object), 400
    except(exc.IntegrityError, ValueError) as e:
        response_object = {
            'status': 'error',
            'message' : 'Invalid payload'
            }
        return jsonify(response_object), 400



@class_blueprint.route('/api/view_chapters/<module_id>', methods=['GET'])
def list_chapters(module_id):
    chapter_list = []
    try:
        chapter_data = Chapters.query.filter_by(module_id=module_id).all()
        print(chapter_data[0].chapter_name)
        
        for i in chapter_data:
            chapter = {}
            chapter['id'] = i.id
            chapter['name'] = i.chapter_name
            chapter['selectDate'] = i.select_date
            chapter['published'] = i.published
            chapter['isCompleted'] = i.completed

            sub_chapters = Subchapters.query.filter_by(chapter_id= i.id).all()
            chapter['subChapter']=[]
            for j in sub_chapters:
                items={
                    'id': j.id,
                    'name': j.name,
                    'selectDate': j.select_date,
                    'published': j.published,
                    'isCompleted': j.completed
                    }
                chapter['subChapter'].append(items)
            chapter_list.append(chapter)
        return jsonify({'status': 'success', 'chapters': chapter_list}),200
    except(exc.IntegrityError, ValueError) as e:
        response_object = {
            'status': 'error',
            'message' : 'Invalid payload'
            }
        return jsonify(response_object), 400

@class_blueprint.route('/api/class/<user_id>', methods=['GET'])
def class_list(user_id):
    uid=user_id
    user = User.query.filter_by(id=uid).first()
    try:
        if user is not None:
            classes_list=[]
            query_class = Classes.query.join(class_user_table).join(User).filter(class_user_table.c.user_id == uid).all()
            for classes in query_class:
                class_details={
                    'class_id': classes.id,
                    'class_name': classes.class_name
                    }
                classes_list.append(class_details)
            return jsonify({'status':'success', 'classes_list': classes_list}),200
        else:
            response_object={
                'status': 'error',
                'message' : 'Inavalid User'
                }
            return jsonify(response_object),400
    except(exc.IntegrityError, ValueError) as e:
        response_object = {
            'status': 'error',
            'message' : 'Invalid payload'
            }
        return jsonify(response_object), 400



@class_blueprint.route('/api/update_chapters/<chapter_id>', methods=['PUT'])
def update_chapters(chapter_id):
    cid = chapter_id
    post_data = request.get_json()
    date = post_data['date']
    print(date)
    try:
        chapter = Chapters.query.filter_by(id = cid).first()
        if chapter is not None:
            print('Updating')
            db.session.query(Chapters).filter_by(id=cid).update({"select_date": date})
            db.session.commit()
            response_object={
                'status': 'success',
                'message': 'chapter Updated successfully'
                }
            return jsonify(response_object), 204
        else:
            response_object={
                'status': 'error',
                'message': 'Something Went wrong'
                }
            return jsonify(response_object), 400
    except(exc.IntegrityError, ValueError) as e:
        response_object = {
            'status': 'error',
            'message' : 'Invalid payload'
            }
        return jsonify(response_object), 400



@class_blueprint.route('/api/update_subchapters/<subchapter_id>', methods=['PUT'])
def update_subchapters(subchapter_id):
    scid = chapter_id
    post_data = request.get_json()
    date = post_data['date']
    try:
        subChapter = Subchapters.query.filter_by(id = scid).first()
        if subChapter is not None:
            db.session.query(Subchapters).filter_by(id=scid).update({"select_date": date})
            db.session.commit()
            response_object={
                'status': 'success',
                'message': 'sub-chapter Updated successfully'
                }
            return jsonify(response_object), 204
        else:
            response_object={
                'status': 'error',
                'message': 'Something Went wrong'
                }
            return jsonify(response_object), 400
    except(exc.IntegrityError, ValueError) as e:
        response_object = {
            'status': 'error',
            'message' : 'Invalid payload'
            }
        return jsonify(response_object), 400



