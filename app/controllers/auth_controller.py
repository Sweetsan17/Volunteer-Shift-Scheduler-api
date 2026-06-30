import re
from flask import jsonify, request
from flask_jwt_extended import create_access_token
from app.extensions import db
from app.models.user_model import User
