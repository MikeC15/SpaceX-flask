import models
from flask import Blueprint, jsonify, request
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import login_user, current_user
from playhouse.shortcuts import model_to_dict


user = Blueprint('users', 'user')