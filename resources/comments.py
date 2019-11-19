from flask import Blueprint, jsonify, request
from flask_login import current_user
from playhouse.shortcuts import model_to_dict
import models

comment = Blueprint('comments', 'comment')

#index route
@comment.route('/', methods=["GET"])
def get_all_comments():
    print('REQUEST.COOKIES:',request.cookies)
    print('CURRENTUSER:',model_to_dict(current_user))
    try:
        comments = [model_to_dict(comment) for comment in models.Comment.select()]
        print("COMMENTS:", comments)
        return jsonify(data=comments, status={"code": 200, "message": "Success"})
    except models.DoesNotExist:
        return jsonify(data={}, status={"code": 401, "message": "Error getting the resources"})

#create route
@comment.route('/', methods=["POST"])
def create_comments():
    payload = request.get_json()
    print("PAYLOAD:", payload)
    print("PAYLOADTYPE:", type(payload))
    #someone must be logged in
    if not current_user.is_authenticated:
        print("CURRENTUSER", current_user)
        return jsonify(data={}, status={"code": 401, "message": "Error getting the resources"})
    payload['user'] = current_user.id
    comment = models.Comment.create(**payload)
    print('COMMENT_DICT:', comment.__dict__)
    print('DIR(COMMENT):', dir(comment))
    print('MODEL_TODICT(COMMENT):', model_to_dict(comment))
    comment_dict = model_to_dict(comment)
    return jsonify(data=comment_dict, status={"code": 201, "message": "Successfully created"})
