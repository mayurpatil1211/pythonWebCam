from flask import Blueprint, jsonify, request
from sqlalchemy import exc, or_
from sqlalchemy import update
#Import from auth module
from app.mod_auth.utils import authenticate
from app.homework.models import *

#import from class_subject
from app.mod_auth.models import *
from app.class_subject.models import *
from app.slides.models import *

from app import db, bcrypt


homework_blueprint = Blueprint('homework', __name__)


# @homework_blueprint.route('/api/questions/<module_id>', methods=['GET'])
# def view_questions(module_id):
#     chapter_list=[]
#     try:
#         module = Modules.query.filter_by(id= module_id).first()
#         if module is not None:
#             chapters_module = Chapters.query.filter_by(module_id=module.id).all()
#             if chapters_module is not None:
#                 for item in chapters_module:
#                     chapter = {}
#                     chapter['id'] = item.id
#                     chapter['name'] = item.chapter_name
#                     chapter['subchapters'] = []

#                     query_chapter_subchapter = Subchapters.query.filter_by(chapter_id=item.id).all()
#                     for sub in  query_chapter_subchapter:
#                         subchapter={}
#                         subchapter['id'] = sub.id
#                         subchapter['name'] = sub.name
#                         subchapter['questions'] = []

#                         query_question_subchapter = Questions.query.filter_by(subchapter_id=sub.id).all()
#                         for i in query_question_subchapter:
#                             question = {
#                                 'qid' : i.id,
#                                 'question': i.question,
#                                 'date': i.date
#                             }
#                             subchapter['questions'].append(question)
#                         chapter['subchapters'].append(subchapter)
#                     chapter_list.append(chapter)
#                 return jsonify({'status': 'success', 'questions':chapter_list}),200
#             else:
#                 response_object={
#                     'status': 'error',
#                     'message': 'Invalid Data please check before sending'
#                 }
#                 return jsonify(response_object), 400
#         else:
#             response_object={
#                 'status':'success',
#                 'message': 'Invalid Data'
#             }
#             return jsonify(response_object), 400
#     except (exc.IntegrityError, ValueError) as e:
#         response_object = {
#             'status':'error',
#             'message':'Inavalid payload'
#         }
#         return jsonify(response_object), 400




# @homework_blueprint.route('/api/update_questions/<question_id>', methods=['PUT'])
# def update_questions(question_id):
#     qid = question_id
#     post_data = request.get_json()
#     date = post_data['date']
#     try:
#         question = Questions.query.filter_by(id = qid).first()
#         if question is not None:
#             db.session.query(Questions).filter_by(id=qid).update({"date": date})
#             db.session.commit()
#             response_object={
#                 'status': 'success',
#                 'message': 'sub-chapter Updated successfully'
#                 }
#             return jsonify({'response':response_object, 'status_code':204})
#         else:
#             response_object={
#                 'status': 'error',
#                 'message': 'Something Went wrong'
#                 }
#             return jsonify(response_object),400
#     except(exc.IntegrityError, ValueError) as e:
#         response_object = {
#             'status': 'error',
#             'message' : 'Invalid payload'
#             }
#         return jsonify(response_object),400



@homework_blueprint.route('/api/homework/create_homework', methods=['POST'])
def create_homework():
    post_data = request.get_json()

    if not post_data:
        response_object = {
            'status': 'error',
            'message': 'Invalid payload'
        }
        return jsonify(response_object), 400

    try:
        class_id = post_data.get('class_id')
        subject_id = post_data.get('subject_id')
        module_id = post_data.get('module_id')
        chapter_id = post_data.get('chapter_id')
        subchapter_id = post_data.get('subchapter_id')
        created_by = post_data.get('user_id')
        homework_date = post_data.get('homework_date')

        if homework_date is not None:
            homework_date_new = homework_date
        else:
            homework_date_new = None

        check_class = Classes.query.filter_by(id=class_id).first()
        check_subject = Subjects.query.filter_by(id=subject_id).first()
        check_module = Modules.query.filter_by(id=module_id).first()
        check_chapter = Chapters.query.filter_by(id = chapter_id).first()
        check_subchapter = Subchapters.query.filter_by(id= subchapter_id).first()
        check_user = User.query.filter_by(id=created_by).first()

        if not any((check_class, check_subject, check_module, check_chapter, check_subchapter, check_user)):
            response_object={
                'status': 'error',
                'message': 'Invalid payload'
            }
            return jsonify(response_object), 400
        else:
            homework_add = Homework(class_id = check_class.id, subject_id = check_subject.id, module_id = check_module.id, chapter_id = check_chapter.id, subchapter_id = check_subchapter.id, created_by = check_user.id, homework_date = homework_date_new)
            db.session.add(homework_add)
            db.session.flush()
            print(homework_add.id)
            homework_obj = {
                'homework_id': homework_add.id,
                'class_id': homework_add.class_id,
                'subject_id': homework_add.subject_id,
                'module_id' : homework_add.module_id,
                'chapter_id': homework_add.chapter_id,
                'subchapter_id': homework_add.subchapter_id
            }
            db.session.commit()
            return jsonify({'status': 'success', 'response_object': homework_obj}), 201
    except(exc.IntegrityError, ValueError) as e:
        response_object = {
            'status': 'error',
            'message' : 'Invalid payload'
            }
        return jsonify(response_object),400


@homework_blueprint.route('/api/homework/<homework_id>/question_answer', methods=['POST'])
def question_homewrok(homework_id):
    post_data = request.get_json()
    if not post_data:
        response_object = {
            'status': 'error',
            'message': 'Inavalid payload'
        }
        return jsonify(response_object), 400
    try:
        print(post_data['QA'])
        question_answer = post_data['QA']
        check_homework = Homework.query.filter_by(id = homework_id).first()
        if check_homework is not None:
            for question in question_answer:
                new_question = (question['question'])
                new_answer = (question['answer'])
                add_question = Questions(question= new_question, homework_id = homework_id)
                db.session.add(add_question)
                db.session.flush()
                add_answer = Answers(answer=new_answer, question_id = add_question.id)
                db.session.add(add_answer)
                db.session.commit()
            response_object={
                'status':'success',
                'message': 'Question and answer created successfully'
            }
            return jsonify(response_object), 201
        else:
            response_object = {
                'status': 'error',
                'message' : 'Something went wrong, Please try again'
            }
            return jsonify(response_object), 400
    except(exc.IntegrityError, ValueError) as e:
        response_object = {
            'status': 'error',
            'message' : 'Invalid payload'
            }
        return jsonify(response_object),400


@homework_blueprint.route('/api/homework/<homework_id>/questions', methods=['GET'])
def get_questions(homework_id):
    check_homework = Homework.query.filter_by(id = homework_id).first()
    try:
        if check_homework is not None:
            questions_list = []
            que_list = Questions.query.filter_by(homework_id = homework_id).all()
            for que in que_list:
                question = {
                    'question': que.question,
                    'id': que.id
                }
                questions_list.append(question)
            return jsonify({'status': 'success', 'questions': questions_list, 'homework_id': homework_id}), 200
        else:
            response_object={
                'status': 'error',
                'message': 'Something Went wrong, please try again letter'
            }
            return jsonify(response_object), 400
    except(exc.IntegrityError, ValueError) as e:
        response_object = {
            'status': 'error',
            'message' : 'Invalid payload'
            }
        return jsonify(response_object),400

# @homework_blueprint.route('/api/homework/<homework_id>/answers', methods=['GET'])
# def get_answer()