#!/usr/bin/env python
import datetime
import logging
import sys

from constants.common import LANGUAGE_ENGLISH
from constants import TRANSLATION
from exceptions import InvalidInput, ProperNotFound
from typing import List, Tuple

import click

import controller
from kalendar.models import Calendar, Day
from propers.models import Proper


def _log_setup(verbosity: int):
    level = {0: logging.WARN, 1: logging.INFO}.get(verbosity, logging.DEBUG)
    logging.basicConfig(
        stream=sys.stdout,
        level=level,
        format='%(asctime)s %(levelname)s: %(message)s')


@click.group()
def cli():
    pass


def _print_proper(language, proper):
    click.echo(f'\n\n============ {language} ============\n\n')
    for section in proper.serialize():
        click.echo(f'\n### {section["label"]}')
        click.echo(section["body"])


@click.command()
@click.argument('year', default=datetime.datetime.now(datetime.timezone.utc).year, type=int)
@click.option('--month', default=None, type=int)
@click.option('--language', default=LANGUAGE_ENGLISH)
@click.option('-v', '--verbosity', count=True)
def calendar(year, language, month, verbosity: int):
    _log_setup(verbosity)
    def _print_all(missal):
        for date_, day in missal.items():
            if month and date_.month != month:
                continue
            if date_.weekday() == 6:
                click.echo("---")
            if date_.day == 1:
                click.echo(f"\n\n# {date_.month}\n")


            padding = 40
            tempora = day.tempora
            celebration = day.celebration
            commemoration = day.commemoration
            rows_count = max([len(tempora), len(celebration), len(commemoration)])
            for row_number in range(0, rows_count):
                collect = []
                for items in (tempora, celebration, commemoration):
                    if not items:
                        collect.append('-')
                    elif len(items) - 1 < row_number:
                        collect.append("")
                    else:
                        repr_ = f"[{items[row_number].name}:{items[row_number].rank}] {items[row_number].title}"
                        if len(repr_) > padding:
                            repr_ = repr_[:padding - 3] + '…'
                        collect.append(repr_)
                te, ce, co = collect
                datestr = date_.strftime('%A %Y-%m-%d') if row_number == 0 else ""
                click.echo(f"{datestr.ljust(22)} class:{str(day.get_celebration_rank()).ljust(6)}"
                           f"{te.ljust(padding)} {ce.ljust(padding)} {co.ljust(padding)}")

    missal: Calendar = controller.get_calendar(year, language)
    _print_all(missal)


@click.command()
@click.argument('proper_id')
@click.option('--language', default=LANGUAGE_ENGLISH)
@click.option('-v', '--verbosity', count=True)
def proper(proper_id: str, language: str, verbosity: int):
    _log_setup(verbosity)
    try:
        proper_vernacular, proper_latin = controller.get_proper_by_id(proper_id, language)
        click.echo('# title Latin: {}'.format(proper_latin.title))
        click.echo('# title vernacular: {}'.format(proper_vernacular.title))
        click.echo('class: {}'.format(proper_latin.rank))
        _print_proper(language, proper_vernacular)
        _print_proper('Latin', proper_latin)
    except (InvalidInput, ProperNotFound) as e:
        sys.stderr.write(str(e))


@click.command()
@click.argument('date')
@click.option('--language', default=LANGUAGE_ENGLISH)
@click.option('-v', '--verbosity', count=True)
def date(date: str, language: str, verbosity: int):
    _log_setup(verbosity)
    yy, mm, dd = date.split('-')
    date_object = datetime.date(int(yy), int(mm), int(dd))
    missal: Calendar = controller.get_calendar(date_object.year, language)
    day: Day = missal.get_day(date_object)
    propers: List[Tuple[Proper, Proper]] = controller.get_proper_by_date(date_object, language)
    click.echo(f'# {date}')
    click.echo('- tempora: {}'.format(day.get_tempora_name()))
    click.echo('- celebration: {}'.format(day.get_celebration_name()))
    click.echo('- class: {}'.format(day.get_celebration_rank()))
    for itr, (proper_vernacular, proper_latin) in enumerate(propers, 1):
        if len(propers) > 1:
            click.echo(f'\n--- Missa {itr} ---')
        if proper_vernacular.description:
            click.echo(f"\n{proper_vernacular.description}")
        _print_proper(language, proper_vernacular)
        _print_proper('Latin', proper_latin)


@click.command()
@click.argument('date_or_id')
@click.option('--language', default=LANGUAGE_ENGLISH)
@click.option('-v', '--verbosity', count=True)
def proper_cols(date_or_id: str, language: str, verbosity: int):
    """
    Print propers in two columns: vernacular (left) and Latin (right).
    Each displayed line is truncated to 50 characters to keep output compact.
    """
    _log_setup(verbosity)
    try: 
        yy, mm, dd = date_or_id.split('-')
        date_object = datetime.date_or_id(int(yy), int(mm), int(dd))
    except Exception:
        proper_id = {i['ref']: i['id'] for i in TRANSLATION[language].VOTIVE_MASSES}.get(date_or_id, date_or_id)
        propers_all = [controller.get_proper_by_id(proper_id, language)]
    else:
        missal: Calendar = controller.get_calendar(date_object.year, language)
        day: Day = missal.get_day(date_object)
        propers_all: List[Tuple[Proper, Proper]] = controller.get_proper_by_date(date_object, language)
        click.echo()
        click.echo(f'# {date_or_id}')
        click.echo('- tempora: {}'.format(day.get_tempora_name()))
        click.echo('- celebration: {}'.format(day.get_celebration_name()))
        comms = day.get_commemorations_titles()
        if comms:
            click.echo('- commemorations:')
            for c in comms:
                click.echo('  - {}'.format(c))
        click.echo('- class: {}'.format(day.get_celebration_rank()))
        click.echo()

    for propers in propers_all:
        vern, lat = propers
        if vern.description:
            click.echo(f"\n{vern.description}")
        click.echo()

        
        sections_all = list(lat.keys())
        for k in vern.keys():
            # not a simple set to maintain order
            if k not in sections_all:
                sections_all.append(k)
        for section_id in sections_all:
            body_len = 60
            padding = body_len + 5
            section_vern = vern.get_section(section_id)
            section_lat = lat.get_section(section_id)

            if section_vern is not None:
                section_vern_label = section_vern.label
                body_vern = section_vern.get_body()
                if section_vern.id.startswith("Evangelium") or section_vern.id.startswith("Lectio"):
                    body_vern.pop(0)
            else:
                body_vern = ["-- missing --"]
                section_vern_label = f"({section_id})"
            
            if section_lat is not None:
                section_lat_label = section_lat.label
                body_lat = section_lat.get_body()
                if section_lat.id.startswith("Evangelium") or section_lat.id.startswith("Lectio"):
                    body_lat.pop(0)
            else:
                body_lat = ["-- missing --"]
                section_lat_label = f"({section_id})"

            body_short_vern = ' '.join(body_vern)[:body_len]
            body_short_lat = ' '.join(body_lat)[:body_len]
            click.echo(f'# {section_vern_label.ljust(padding - 2)} # {section_lat_label.ljust(padding)}')
            click.echo(f'{body_short_vern.ljust(padding)} {body_short_lat.ljust(padding)}')
            click.echo()
        click.echo("---")


@click.command()
def ical():
    click.echo(controller.get_ical(LANGUAGE_ENGLISH))


cli.add_command(calendar)
cli.add_command(date)
cli.add_command(proper_cols)
cli.add_command(proper)
cli.add_command(ical)


if __name__ == '__main__':
    cli()
