from flask import render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from . import message_board
from .. import db
from ..models import Role, User, ReserveInfo





