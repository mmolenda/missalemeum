import json
import os

import datetime
import sys

import logging
from flask import render_template, Blueprint

import controller
from constants.common import LANGUAGE_VERNACULAR
from kalendar.models import Day

logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format="[%(asctime)s ] %(levelname)s in %(module)s: %(message)s")


views = Blueprint("views", __name__)


@views.route("/")
@views.route("/<string:date_>")
def proprium(date_: str = None):
    try:
        date_object = datetime.datetime.strptime(date_, "%Y-%m-%d").date()
        day: Day = controller.get_day(date_object, LANGUAGE_VERNACULAR)
    except Exception:
        title = None
        date_ = None
    else:
        title = day.get_celebration_name()
    return render_template("proprium.html", title=title, date=date_)


@views.route("/ordo")
def ordo():
    with open(os.path.join(views.root_path, "static", "data", "ordo.json")) as fh:
        ordo_data = json.load(fh)
    return render_template("ordo.html", title="Części stałe", data=ordo_data)


@views.route("/icalendar")
def icalendar():
    return render_template("icalendar.html", title="iCalendar")


@views.route("/info")
def info():
    return render_template("info.html", title="Informacje")
