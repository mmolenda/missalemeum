import json
from collections import defaultdict
from functools import wraps

import mistune
import os

import datetime
import sys

import logging
import re
from flask import render_template, Blueprint, request, send_from_directory, redirect, render_template_string
from jinja2 import TemplateNotFound

import controller
from constants.common import LANGUAGE_VERNACULAR
from exceptions import SupplementNotFound
from kalendar.models import Day
from settings import LANGUAGES
from utils import format_propers, get_supplement

logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format="[%(asctime)s ] %(levelname)s in %(module)s: %(message)s")

log = logging.getLogger(__name__)


views = Blueprint("views", __name__)


def render_template_or_404(template, lang, **context):
    try:
        return render_template(template, lang=lang, **context)
    except TemplateNotFound:
        return render_template('404.html', lang=lang), 404


def infer_locale(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'lang' not in kwargs:
            kwargs['lang'] = request.accept_languages.best_match(LANGUAGES.keys())
        return f(*args, **kwargs)
    return decorated_function


@views.route("/")
@views.route("/<string:date_>")
@views.route("/<lang:lang>")
@views.route("/<lang:lang>/<string:date_>")
@infer_locale
def proprium(lang: str = LANGUAGE_VERNACULAR, date_: str = None):
    if date_ is not None:
        try:
            date_object = datetime.datetime.strptime(date_, "%Y-%m-%d").date()
            day: Day = controller.get_day(date_object, lang)
            fmt_propers = format_propers(day)
        except Exception as e:
            log.exception(e)
            return render_template('404.html', lang=lang), 404
        else:
            title = fmt_propers[0]['info']['title']
    else:
        title = None
        date_ = None
        fmt_propers = None
    return render_template("proprium.html", title=title, propers=fmt_propers, date=date_, proper_active=True, lang=lang)


@views.route("/ordo")
@views.route("/<string:lang>/ordo")
@infer_locale
def ordo(lang: str = LANGUAGE_VERNACULAR):
    with open(os.path.join(views.root_path, "static", "data", lang, "ordo.json")) as fh:
        data = json.load(fh)
    return render_template("ordo.html", data=data, lang=lang)


class CanticumIndex:
    index = defaultdict(list)

    def get(self, lang):
        if lang not in self.index:
            try:
                filenames = os.listdir(os.path.join(views.root_path, "supplement", lang, "canticum"))
            except FileNotFoundError:
                raise SupplementNotFound
            else:
                for filename in sorted(filenames):
                    resource_id = filename.rsplit('.', 1)[0]
                    index_item = get_supplement(views.root_path, lang, resource_id, "canticum")
                    self.index[lang].append(
                        {"title": index_item["title"],
                         "ref": resource_id,
                         "tags": index_item["tags"]
                         })
        return self.index[lang]


canticum_index = CanticumIndex()


@views.route("/canticum")
@views.route("/canticum/<string:canticum_id>")
@views.route("/<string:lang>/canticum")
@views.route("/<string:lang>/canticum/<string:canticum_id>")
@infer_locale
def canticum(lang: str = LANGUAGE_VERNACULAR, canticum_id: str = None):
    index = canticum_index.get(lang)
    title = None
    if canticum_id is not None:
        for i in index:
            if i["ref"] == canticum_id:
                title = i["title"]
                break
    return render_template("canticum.html", title=title, index=index, lang=lang)


@views.route("/supplement")
@views.route("/supplement/<string:resource>")
@views.route("/supplement/<subdir>/<string:resource>")
@views.route("/<string:lang>/supplement")
@views.route("/<string:lang>/supplement/<string:resource>")
@views.route("/<string:lang>/supplement/<subdir>/<string:resource>")
@infer_locale
def supplement(lang: str = LANGUAGE_VERNACULAR, subdir: str = None, resource: str = None):
    if resource is None:
        return render_template_or_404(f"{lang}/supplement-main.html", lang=lang)
    try:
        supplement_yaml = get_supplement(views.root_path, lang, resource, subdir)
    except SupplementNotFound:
        return render_template_or_404("404.html", lang=lang), 404
    else:
        title = supplement_yaml["title"]
        html = mistune.markdown(supplement_yaml["body"], escape=False)
        ref = request.args.get("ref")
        if ref is None or re.sub('[\w\-/]', '', ref) != "":
            ref = None
        return render_template_or_404(f"{lang}/supplement.html", title=title, data=html, ref=ref, lang=lang)


@views.route("/icalendar")
def icalendar():
    return redirect("/supplement", code=302)


@views.route("/info")
@views.route("/<string:lang>/info")
@infer_locale
def info(lang: str = LANGUAGE_VERNACULAR):
    return render_template_or_404(f"{lang}/info.html", lang=lang)


@views.route("/tmp/rorate")
@infer_locale
def rorate(lang: str = LANGUAGE_VERNACULAR):
    return render_template_or_404(f"rorate.html", lang=lang)


@views.route("/service-worker.js")
def service_worker():
    return send_from_directory(os.path.join(views.root_path, "static", "js"), "service-worker.js")


@views.route("/robots.txt")
def robots():
    return render_template_string("User-agent: *\nDisallow:")
