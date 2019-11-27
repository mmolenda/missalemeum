import json
import markdown
import os

import datetime
import sys

import logging
import re
from flask import render_template, Blueprint, request, send_from_directory, redirect, render_template_string
from jinja2 import TemplateNotFound

import controller
from constants.common import LANGUAGE_VERNACULAR
from kalendar.models import Day
from utils import format_propers

logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format="[%(asctime)s ] %(levelname)s in %(module)s: %(message)s")

log = logging.getLogger(__name__)


views = Blueprint("views", __name__)


def render_template_or_404(template, **context):
    try:
        return render_template(template, **context)
    except TemplateNotFound:
        return render_template('404.html'), 404


@views.route("/")
@views.route("/<string:date_>")
# @views.route("/<string:lang>")
# @views.route("/<string:lang>/<string:date_>")
def proprium(lang: str = LANGUAGE_VERNACULAR, date_: str = None):
    if date_ is not None:
        try:
            date_object = datetime.datetime.strptime(date_, "%Y-%m-%d").date()
            day: Day = controller.get_day(date_object, lang)
            fmt_propers = format_propers(day)
        except Exception as e:
            log.exception(e)
            return render_template('404.html'), 404
        else:
            title = fmt_propers[0]['info']['title']
    else:
        title = None
        date_ = None
        fmt_propers = None
    return render_template("proprium.html", title=title, propers=fmt_propers, date=date_, proper_active=True, lang=lang)


@views.route("/ordo")
# @views.route("/<string:lang>/ordo")
def ordo(lang: str = LANGUAGE_VERNACULAR):
    with open(os.path.join(views.root_path, "static", "data", "ordo.json")) as fh:
        data = json.load(fh)
    return render_template("ordo.html", data=data, lang=lang)


@views.route("/supplement")
@views.route("/supplement/<string:resource>")
@views.route("/supplement/<subdir>/<string:resource>")
# @views.route("/<string:lang>/supplement")
# @views.route("/<string:lang>/supplement/<string:resource>")
# @views.route("/<string:lang>/supplement/<subdir>/<string:resource>")
def supplement(lang: str = LANGUAGE_VERNACULAR, subdir: str = None, resource: str = None):
    if resource is None:
        return render_template_or_404(f"{lang}/supplement-main.html", lang=lang)

    try:
        path_args = [views.root_path, "supplement", lang]
        if subdir:
            path_args.append(subdir)
        path_args.append(f"{resource}.md")
        with open(os.path.join(*path_args)) as fh:
            md = fh.read()
            html = markdown.markdown(md, extensions=['tables'])
            title = [i for i in md.split("\n") if i.startswith("#")][0].strip(" #")
    except IOError:
        return render_template_or_404('404.html'), 404
    else:
        ref = request.args.get("ref")
        if ref is None or re.sub('[\w\-/]', '', ref) != "":
            ref = None
        return render_template_or_404(f"{lang}/supplement.html", title=title, data=html, ref=ref, lang=lang)


@views.route("/icalendar")
def icalendar():
    return redirect("/supplement", code=302)


@views.route("/info")
# @views.route("/<string:lang>/info")
def info(lang: str = LANGUAGE_VERNACULAR):
    return render_template_or_404(f"{lang}/info.html", lang=lang)


@views.route("/service-worker.js")
def service_worker():
    return send_from_directory(os.path.join(views.root_path, "static", "js"), "service-worker.js")


@views.route("/robots.txt")
def robots():
    return render_template_string("User-agent: *\nDisallow:")
