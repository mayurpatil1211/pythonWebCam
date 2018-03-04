from flask import Blueprint, jsonify, request
from sqlalchemy import exc, or_
from sqlalchemy import update
from werkzeug.datastructures import CombinedMultiDict, MultiDict
from datetime import datetime
#Import from auth module
from app.mod_auth.utils import authenticate
from app.slides.models import *

#import from class_subject and user
from app.class_subject.models import *
from app.mod_auth.models import *
from app.homework.models import *

from app import db, bcrypt


slides_blueprint = Blueprint('slides', __name__)


@slides_blueprint.route('/api/update_slides/<user_id>/<slide_id>',  methods=['PUT'])
def update_slide(user_id,slide_id):
    post_data=request.get_json()
    if not post_data:
        response_object={
            'status': 'error',
            'message': 'Invalid payload'
            }
        return jsonify(response_object), 400
    date = post_data['date']
    try:
        user = User.query.filter_by(id=user_id).first()
        if user is not None:
            slide = Slides.query.filter_by(id=slide_id).first()
            if slide is not None:
                db.session.query(User_slides).filter_by(sid=slide.id, uid = user.id).update({"date": date})
                db.session.commit()
                response_object = {
                    'status': 'Success',
                    'message': 'Updated Successfully'
                    }
                return jsonify(response_object),200
            else:
                response_object = {
                    'status': 'error',
                    'message': 'Somethnig went wrong, please contact administrator'
                    }
                return jsonify(response_object), 400
        else:
            response_object={
                'status': 'error',
                'message': 'Something went wrong, please contact administrator'
                }
            return jsonify(response_object), 400
    except(exc.IntegrityError, ValueError) as e:
        response_object = {
            'status': 'error',
            'message' : 'Invalid payload'
            }
        return jsonify(response_object), 400


# @slides_blueprint.route('/create/slides')

# @slides_blueprint.route('/api/slide/<subchapter_id>', methods=['GET'])
# def watch_slide(subchapter_id):
#     slides = Slides.query.filter_by(subchapter_id=subchapter_id).all()
#     div = ''
#     for slide in slides:
#         print(slide.heading)
#         line = slide.heading
#         line = line.replace('\n', ' ')
#         print(slide.contents)
#         cont = slide.contents
#         cont = cont.replace('\n', ' ')
#         div += "<div> {}{}</div>".format(line, cont)
#     return jsonify({"html": '''
#             <html>
#               <head>
#                 <title>Home Page</title>
#               </head>
#               <body>
#                 <h1>Hello {}</h1>
#               </body>
#             </html>
#             '''.format(div)})



@slides_blueprint.route('/api/slide1/<subchapter_id>', methods=['GET'])
def watch_slide1(subchapter_id):
    slides = Slides.query.filter_by(subchapter_id=subchapter_id).all()
    div = ''
    for slide in slides:
        print(slide.id)
        print(slide.subchapter_id)
        print(slide.heading)
        print(slide.contents)
        div += "<section id={}> {}{}</section>".format(slide.id, slide.heading, slide.contents)
    return '''
            <html>
              <head>
                <title>Home Page</title>
              </head>
              <body>
                <h1>Hello '''+ div +'''</h1>
              </body>
            </html>'''


@slides_blueprint.route('/api/create_slide', methods=['POST'])
def check_slides():
    post_data=request.values
    post_data1=request.get_data()
    print(post_data1)
    if not post_data:
        response_object={
            'status': 'error',
            'message' : 'Invalid payload'
        }
        return jsonify(response_object), 400
    print(post_data['nestnum'])
    print(post_data['hiddenContent'])
    print(post_data['bgcolor'])
    print(post_data['slidenum'])
    print(post_data['trans'])
    print(post_data['update'])

    nestnum = post_data['nestnum']
    hiddenContent = post_data['hiddenContent']
    bgcolor = post_data['bgcolor']
    slidenum = post_data['slidenum']
    trans = post_data['trans']


    try:
        slide_data = Slides(
            heading = 'testing',
            contents = hiddenContent, 
            slide_number = slidenum, 
            nestnumber = nestnum, 
            transition = trans, 
            backgroundColor = bgcolor, 
            subchapter_id = '1'
            )
        db.session.add(slide_data)
        db.session.commit()
        response_object = {
            'status': 'success',
            'message': 'Slide created Successfully'
        }
        return jsonify(response_object),201
    except(exc.IntegrityError, ValueError) as e:
        response_object = {
            'status': 'error',
            'message' : 'Invalid payload'
            }
        return jsonify(response_object), 400


@slides_blueprint.route('/api/slides', methods=['GET'])
def list_slides():
    slides = []
    try:
        list_slide = Slides.query.all()
        if len(list_slide) > 0:
            for item in list_slide:
                slide = {'id': item.id, 'name': item.heading}
                slides.append(slide)
            return (jsonify({'status': 'success',
                    'subjects_list': slides}), 200)
        else:
            response_object = {'status': 'error',
                               'message': 'Something Went Wrong please contact administrator'}
            return (jsonify(response_object), 400)
    except (exc.IntegrityError, ValueError), e:
        response_object = {'status': 'error',
                           'message': 'Invalid payload'}
        return (jsonify(response_object), 400)




@slides_blueprint.route('/api/slide/<slide_id>', methods=['GET'])
def slide_view(slide_id):
    slide_data = Slides.query.filter_by(id=slide_id).first()
    if not slide_data:
        response_object = {'status': 'error',
                           'message': 'Invalid payload'}
        return (jsonify(response_object), 400)
    try:
        if slide_data:
            line = slide_data.contents
            line = line.replace('\n', ' ')
            line = line.replace('\\', '')
            slide = {
                'id': slide_data.id,
                'heading': slide_data.heading,
                'contents': line,
                'backgroundColor': slide_data.backgroundColor,
                'transition': slide_data.transition,
                'subchapter_id': slide_data.subchapter_id,
                }
            return (jsonify({'status': 'success', 'slide': slide}), 200)
        else:
            response_object = {'status': 'error',
                               'message': 'Something went wrong'}
            return (jsonify(response_object), 400)
    except (exc.IntegrityError, ValueError), e:
        response_object = {'status': 'error',
                           'message': 'Invalid payload'}
        return (jsonify(response_object), 400)



# def teach_slide(user_id):
#     teach_slides = []
#     user = User.query.filter_by(id=user_id).first()
#     if not user:
#         response_object={
#             'status':'error',
#             'message': 'Invalid payload'
#         }
#         return jsonify(response_object), 400
#     try:
#         todays_date = datetime.datetime.today().strftime('%d-%m-%Y')
        
#         todays_date = str(todays_date)
#         print (todays_date)
#         user_slide = User_slides.query.filter_by(uid=user_id, date=todays_date).all()
#         if user_slide:
#             for slide_id in user_slide:
#                 slide = Slides.query.filter_by(id=slide_id.id).first()
#                 slide_data = {
#                     'slide_id': slide.id,
#                     'name': slide.heading
#                 }
#                 teach_slides.append(slide_data)
#             return jsonify({'status': 'success', 'slides': teach_slides}), 200
#         else:
#             response_object={
#                 'status': 'error',
#                 'message': 'Sorry, No slides available for this User'
#             }
#             return jsonify(response_object), 400
    # except (exc.IntegrityError, ValueError), e:
    #     response_object = {
    #         'status': 'error',
    #         'message': 'Invalid payload'
    #     }
    #     return jsonify(response_object), 400

@slides_blueprint.route('/api/teach/<user_id>/<class_id>/<subject_id>/<module_id>/<chapter_id>', methods=['GET'])
def teach_slide(user_id, class_id, subject_id, module_id, chapter_id):
    teach_slide = []
    user = User.query.filter_by(id=user_id).first()
    if not user:
        response_object={
            'status': 'error',
            'message': 'Invalid payload'
        }
        return jsonify(response_object), 400
    try:
        todays_date = datetime.datetime.today().strftime('%d-%m-%Y')
        todays_date = str(todays_date)
        module = Modules.query.filter_by(id=module_id, class_id=class_id, subject_id=subject_id).first()
        if module:
            chapter = Chapters.query.filter_by(id=chapter_id, module_id=module_id).first()
            if chapter:
                subchapter = Subchapters.query.filter_by(chapter_id=chapter_id).all()
                for sub in subchapter:
                    slides = Slides.query.filter_by(subchapter_id=sub.id).all()
                    # print(len(slides))
                    for slide in slides:
                        # print('slide id',slide.id)
                        # print('user id',user_id)

                        user_slides = User_slides.query.filter_by(sid=slide.id, uid=user_id, date=todays_date).all()
                        print(user_slides)
                        for user_slide in user_slides:

                            slide_item = Slides.query.filter_by(id=user_slide.sid).first()
                            slide_data = {
                                'slide_id': slide_item.id,
                                'slide_name': slide_item.heading,
                                'date': user_slide.date
                            }
                            teach_slide.append(slide_data)
                return jsonify({'status':'success', 'slides': teach_slide}), 200
            else:
                response_object={
                'status': 'error',
                'message': 'Something went wrong'
                }
                return jsonify(response_object), 400

        else:
            response_object={
                'status': 'error',
                'message': 'Something went wrong'
            }
            return jsonify(response_object), 400
    except (exc.IntegrityError, ValueError), e:
        response_object = {
            'status': 'error',
            'message': 'Invalid payload'
        }
        return jsonify(response_object), 400