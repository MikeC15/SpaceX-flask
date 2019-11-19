from flask import Blueprint, jsonify, request
from flask_login import current_user
from playhouse.shortcuts import model_to_dict
import models

comment = Blueprint('comments', 'comment')

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