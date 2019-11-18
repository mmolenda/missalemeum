import json
import markdown
import os

import datetime
import sys

import logging
from flask import render_template, Blueprint, request

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
    if date_ is not None:
        try:
            date_object = datetime.datetime.strptime(date_, "%Y-%m-%d").date()
            day: Day = controller.get_day(date_object, LANGUAGE_VERNACULAR)
        except Exception:
            return render_template('404.html', title="404"), 404
        else:
            title = day.get_celebration_name()
    else:
        title = None
        date_ = None
    return render_template("proprium.html", title=title, date=date_)


@views.route("/ordo")
def ordo():
    with open(os.path.join(views.root_path, "static", "data", "ordo.json")) as fh:
        data = json.load(fh)
    return render_template("ordo.html", title="Części stałe", data=data)


@views.route("/supplement/<string:resource>")
def supplement(resource: str):
    try:
        with open(os.path.join(views.root_path, "supplement", f"{resource}.md")) as fh:
            md = fh.read()
            html = markdown.markdown(md)
            title = resource.replace("-", " ")
    except IOError:
        return render_template('404.html'), 404
    else:
        ref_date = None
        if "ref" in request.args:
            try:
                datetime.datetime.strptime(request.args["ref"], "%Y-%m-%d")
            except ValueError as e:
                pass
            else:
                ref_date = request.args["ref"]
        return render_template("supplement.html", title=title, data=html, ref_date=ref_date)


@views.route("/icalendar")
def icalendar():
    return render_template("icalendar.html", title="iCalendar")


@views.route("/info")
def info():
    return render_template("info.html", title="Informacje")
