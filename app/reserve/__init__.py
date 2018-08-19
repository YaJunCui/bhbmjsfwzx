from flask import Blueprint

auth = Blueprint('reverse', __name__)

from . import views