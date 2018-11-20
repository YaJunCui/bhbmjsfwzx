from flask import render_template, redirect, url_for
from flask_login import login_required, current_user
from . import reserve
from .forms import ReserveInfoForm
from ..models import Role, User


@reserve.route('/add_reserve', methods=["GET", "POST"])
@login_required
def add_reserve():
    user = User.query.get_or_404(current_user.id)
    form = ReserveInfoForm(user=user)
    return render_template("reserve/add_reserve.html", form=form)