from flask import render_template, redirect, url_for
from flask_login import login_required
from . import reserve


@reserve.route('/add_reserve', method=["GET", "POST"])
@login_required
def add_reserve():
    pass