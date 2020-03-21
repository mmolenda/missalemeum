#!/usr/bin/env python
import datetime
import logging
import sys

from constants.common import LANGUAGE_ENGLISH
from exceptions import InvalidInput, ProperNotFound
from typing import List, Tuple

import click

import controller
from kalendar.models import Calendar, Day
from propers.models import Proper


logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s')


@click.group()
def cli():
    pass


def _print_proper(language, proper):
    click.echo(f'\n=== {language} ===\n')
    for section in proper.serialize():
        click.echo(f'\n== {section["label"]} ==')
        click.echo(section["body"])


@click.command()
@click.argument('year', default=datetime.datetime.utcnow().year, type=int)
@click.option('--language', default=LANGUAGE_ENGLISH)
def calendar(year, language):
    def _print_all(missal):
        for date_, day in missal.items():
            if date_.weekday() == 6:
                click.echo("---")
            if date_.day == 1:
                click.echo(f"\n\n=== {date_.month} ===\n")

            collect = []
            padding = 40
            for i in ('tempora', 'celebration', 'commemoration'):
                items = getattr(day, i, None)
                if not items:
                    collect.append('-')
                else:
                    repr_ = f"[{items[0].name}:{items[0].rank}] {items[0].title}"
                    if len(repr_) > padding:
                        repr_ = repr_[:padding - 3] + '…'
                    collect.append(repr_)
            te, ce, co = collect
            click.echo(f"{date_.strftime('%A %Y-%m-%d').ljust(padding)} "
                       f"{te.ljust(padding)} {ce.ljust(padding)} {co.ljust(padding)}")

    missal: Calendar = controller.get_calendar(year, language)
    _print_all(missal)


@click.command()
@click.argument('proper_id')
@click.option('--language', default=LANGUAGE_ENGLISH)
def proper(proper_id: str, language: str):
    try:
        proper_vernacular, proper_latin = controller.get_proper_by_id(proper_id, language)
        _print_proper(language, proper_vernacular)
        _print_proper('Latin', proper_latin)
    except (InvalidInput, ProperNotFound) as e:
        sys.stderr.write(str(e))


@click.command()
@click.argument('date')
@click.option('--language', default=LANGUAGE_ENGLISH)
def date(date: str, language: str):
    yy, mm, dd = date.split('-')
    date_object = datetime.date(int(yy), int(mm), int(dd))
    missal: Calendar = controller.get_calendar(date_object.year, language)
    day: Day = missal.get_day(date_object)
    propers: List[Tuple[Proper, Proper]] = controller.get_proper_by_date(date_object, language)
    click.echo(f'=== {date} ===')
    click.echo('tempora: {}'.format(day.get_tempora_name()))
    click.echo('celebration: {}'.format(day.get_celebration_name()))
    for itr, (proper_vernacular, proper_latin) in enumerate(propers, 1):
        if len(propers) > 1:
            click.echo(f'\n--- Missa {itr} ---')
        click.echo(proper_vernacular.serialize()[0]['body'][0])
        _print_proper(language, proper_vernacular)
        _print_proper('Latin', proper_latin)


@click.command()
def ical():
    click.echo(controller.get_ical(LANGUAGE_ENGLISH))


cli.add_command(calendar)
cli.add_command(date)
cli.add_command(proper)
cli.add_command(ical)


if __name__ == '__main__':
    cli()
