from flask import Blueprint

message_board = Blueprint('message_board', __name__)

from . import views