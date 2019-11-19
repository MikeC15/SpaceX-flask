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

# show route
@comment.route('/<id>', methods=['GET'])
def get_one_comment(id):
    print("COMMENT-ID:",id)
    comment = models.Comment.get_by_id(id)
    return jsonify(data=model_to_dict(comment), status={"code": 200, "message": "success"})

#delete route HITS ROUTE BUT NOT ACTUALLY DELETING
@comment.route('/<id>', methods=["DELETE"])
def delete_comment(id):
    comment_to_delete = models.Comment.get(id=id)
    if not current_user.is_authenticated: # Checks if user is logged in
        return jsonify(data={}, status={'code': 401, 'message': 'You must be logged in to delete a comment'})
    if comment_to_delete.user.id is not current_user.id: 
        return jsonify(data={}, status={'code': 401, 'message': 'You can only delete comments you wrote'})
    # Delete the comment and send success response back to user
    print("DELETED:", comment_to_delete)
    comment_to_delete.delete_instance()
    return jsonify(data='comment successfully deleted', status={"code": 200, "message": "comment deleted successfully"})

#update route???