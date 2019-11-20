import json
import markdown
import os

import datetime
import sys

import logging
import re
from flask import render_template, Blueprint, request, send_from_directory, redirect

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
            return render_template('404.html'), 404
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
    return render_template("ordo.html", data=data)


@views.route("/supplement")
@views.route("/supplement/<string:resource>")
def supplement(resource: str = None):
    if resource is None:
        return render_template("supplement-main.html")

    try:
        with open(os.path.join(views.root_path, "supplement", f"{resource}.md")) as fh:
            md = fh.read()
            html = markdown.markdown(md)
            title = [i for i in md.split("\n") if i.startswith("#")][0].strip(" #")
    except IOError:
        return render_template('404.html'), 404
    else:
        ref = request.args.get("ref")
        if ref is None or re.sub('[\w\-/]', '', ref) != "":
            ref = None
        return render_template("supplement.html", title=title, data=html, ref=ref)


@views.route("/icalendar")
def icalendar():
    return redirect("/supplement", code=302)


@views.route("/info")
def info():
    return render_template("info.html")


@views.route("/service-worker.js")
def service_worker():
    return send_from_directory(os.path.join(views.root_path, "static", "js"), "service-worker.js")
