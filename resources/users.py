import models
from flask import Blueprint, jsonify, request
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import login_user, current_user
from playhouse.shortcuts import model_to_dict


user = Blueprint('users', 'user')

@user.route('/register', methods=["POST"])
def register():
    payload = request.get_json()
    if not payload['email'] or not payload['password']:
        return jsonify(status=400)
    try:
        # ** is a case insensitive ==
        models.User.get(models.User.email ** payload['email'])
        return jsonify(data={}, status={"code": 400, "message": "A user with that email already exists."})
    except models.DoesNotExist: 
        payload['password'] = generate_password_hash(payload['password'])
        new_user = models.User.create(**payload)
        login_user(new_user)
        user_dict = model_to_dict(new_user)
        print('user_dict:',user_dict)
        print(type(user_dict))
        del user_dict['password']
        return jsonify(data=user_dict, status={'code': 201, 'message': 'User created'})