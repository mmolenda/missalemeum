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
from flask_babel import _
from jinja2 import TemplateNotFound

import controller
from constants import TRANSLATION
from constants.common import LANGUAGE_ENGLISH, SUPPLEMENT_DIR
from exceptions import SupplementNotFound
from kalendar.models import Day
from constants.common import LANGUAGES
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
        if 'lang' in kwargs:
            if kwargs['lang'] not in LANGUAGES.keys():
                return render_template('404.html', lang=LANGUAGE_ENGLISH), 404
        else:
            kwargs['lang'] = request.accept_languages.best_match(LANGUAGES.keys())
        return f(*args, **kwargs)
    return decorated_function


@views.route("/")
@views.route("/<string:date_>")
@views.route("/<lang:lang>")
@views.route("/<lang:lang>/<string:date_>")
@infer_locale
def proprium(lang: str = LANGUAGE_ENGLISH, date_: str = None):
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
def ordo(lang: str = LANGUAGE_ENGLISH):
    with open(os.path.join(views.root_path, "static", "data", lang, "ordo.json")) as fh:
        data = json.load(fh)
    return render_template("ordo.html", data=data, lang=lang)


class SupplementIndex:
    CANTICUM = "canticum"
    ORATIO = "oratio"
    index = defaultdict(list)

    def get_canticum_index(self, lang):
        return self._get_index(lang, self.CANTICUM)

    def get_canticum_title(self, lang, proper_id):
        return self._get_title(lang, self.CANTICUM, proper_id)

    def get_oratio_index(self, lang):
        return self._get_index(lang, self.ORATIO)

    def get_oratio_title(self, lang, proper_id):
        return self._get_title(lang, self.ORATIO, proper_id)

    def _get_index(self, lang, subdir):
        key = f"{lang}-{subdir}"
        if key not in self.index:
            try:
                filenames = os.listdir(os.path.join(SUPPLEMENT_DIR, lang, subdir))
            except FileNotFoundError:
                filenames = []
            finally:
                for filename in sorted(filenames):
                    if filename.endswith(".yaml"):
                        resource_id = filename.rsplit('.', 1)[0]
                        index_item = get_supplement(lang, resource_id, subdir)
                        self.index[key].append(
                            {"title": index_item["title"],
                             "ref": f"{subdir}/{resource_id}",
                             "tags": index_item["tags"]
                             })
        return self.index[key]

    def _get_title(self, lang, subdir, proper_id):
        for i in self._get_index(lang, subdir):
            if proper_id is not None and i["ref"].endswith(proper_id):
                return i["title"]


supplement_index = SupplementIndex()


@views.route("/canticum")
@views.route("/canticum/<string:proper_id>")
@views.route("/<string:lang>/canticum")
@views.route("/<string:lang>/canticum/<string:proper_id>")
@infer_locale
def canticum(lang: str = LANGUAGE_ENGLISH, proper_id: str = None):
    index = supplement_index.get_canticum_index(lang)
    title = supplement_index.get_canticum_title(lang, proper_id) or _("Songs")
    return render_template("supplement_nested.html", title=title, index=index, lang=lang)


@views.route("/oratio")
@views.route("/oratio/<string:proper_id>")
@views.route("/<string:lang>/oratio")
@views.route("/<string:lang>/oratio/<string:proper_id>")
@infer_locale
def oratio(lang: str = LANGUAGE_ENGLISH, proper_id: str = None):
    index = supplement_index.get_oratio_index(lang)
    title = supplement_index.get_oratio_title(lang, proper_id) or _("Prayers")
    return render_template("supplement_nested.html", title=title, index=index, lang=lang)


@views.route("/votive")
@views.route("/votive/<string:proper_id>")
@views.route("/<string:lang>/votive")
@views.route("/<string:lang>/votive/<string:proper_id>")
@infer_locale
def votive(lang: str = LANGUAGE_ENGLISH, proper_id: str = None):
    index = TRANSLATION[lang].VOTIVE_MASSES
    title = None
    if proper_id is not None:
        for i in index:
            if i["ref"] == proper_id:
                title = i["title"]
                break
    return render_template("votive.html", title=title, index=index, lang=lang)


@views.route("/supplement")
@views.route("/supplement/<string:resource>")
@views.route("/supplement/<subdir>/<string:resource>")
@views.route("/<string:lang>/supplement")
@views.route("/<string:lang>/supplement/<string:resource>")
@views.route("/<string:lang>/supplement/<subdir>/<string:resource>")
@infer_locale
def supplement(lang: str = LANGUAGE_ENGLISH, subdir: str = None, resource: str = None):
    if resource is None:
        return render_template_or_404(f"{lang}/supplement-main.html", lang=lang)
    try:
        supplement_yaml = get_supplement(lang, resource, subdir)
    except SupplementNotFound:
        return render_template_or_404("404.html", lang=lang), 404
    else:
        title = supplement_yaml["title"]
        html = mistune.markdown(supplement_yaml["body"], escape=False)
        ref = request.args.get("ref")
        if ref is None or re.sub('[\w\-/]', '', ref) != "":
            ref = None
        return render_template_or_404("supplement.html", title=title, data=html, ref=ref, lang=lang)


@views.route("/icalendar")
def icalendar():
    return redirect("/supplement", code=302)


@views.route("/info")
@views.route("/<string:lang>/info")
@infer_locale
def info(lang: str = LANGUAGE_ENGLISH):
    return render_template_or_404(f"{lang}/info.html", lang=lang)


@views.route("/service-worker.js")
def service_worker():
    return send_from_directory(os.path.join(views.root_path, "static", "js"), "service-worker.js")


@views.route("/robots.txt")
def robots():
    return render_template_string("User-agent: *\nDisallow:")
