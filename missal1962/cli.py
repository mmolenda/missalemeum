#!/usr/bin/env python
import sys

import click
import datetime
import importlib
import logging

from exceptions import InvalidInput, ProperNotFound
from kalendar.factory import MissalFactory
from propers.parser import ProperParser

default_language = 'Polski'


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
        click.echo('\n'.join(section["body"]))


@click.command()
@click.argument('year', default=datetime.datetime.utcnow().year, type=int)
@click.option('--language', default=default_language)
def calendar(year, language):
    def _print_all(missal):
        for date_, lit_day_container in missal.items():
            if date_.weekday() == 6:
                click.echo("---")
            if date_.day == 1:
                click.echo(f"\n\n=== {date_.month} ===\n")

            collect = []
            padding = 40
            for i in ('tempora', 'celebration', 'commemoration'):
                items = getattr(lit_day_container, i, None)
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

    missal = MissalFactory.create(year, language)
    _print_all(missal)


@click.command()
@click.argument('proper_id')
@click.option('--language', default=default_language)
def proper(proper_id, language):
    try:
        proper_vernacular, proper_latin = ProperParser.parse(proper_id, language)
        _print_proper(language, proper_vernacular)
        _print_proper('Latin', proper_latin)
    except (InvalidInput, ProperNotFound) as e:
        sys.stderr.write(str(e))


@click.command()
@click.argument('date')
@click.option('--language', default=default_language)
def date(date, language):
    yy, mm, dd = date.split('-')
    date_object = datetime.date(int(yy), int(mm), int(dd))
    missal = MissalFactory.create(date_object.year, language)
    lit_day_container = missal.get_day(date_object)
    propers = lit_day_container.get_proper()
    click.echo(f'=== {date} ===')
    click.echo('tempora: {}'.format(lit_day_container.get_tempora_name()))
    click.echo('celebration: {}'.format(lit_day_container.get_celebration_name()))
    for itr, (vernacular, latin) in enumerate(propers, 1):
        if len(propers) > 1:
            click.echo(f'\n--- Missa {itr} ---')
        click.echo(vernacular.serialize()[0]['body'][0])
        _print_proper(language, vernacular)
        _print_proper('Latin', latin)


@click.command()
@click.argument('search_string')
@click.option('--language', default=default_language)
def search(search_string, language):
    titles = importlib.import_module(f'constants.{language}.translation')
    for id_, title in titles.titles.items():
        if search_string.strip().lower() in title.lower():
            click.echo(f"{':'.join(id_.split(':')[:2])} {title}")


cli.add_command(calendar)
cli.add_command(date)
cli.add_command(proper)
cli.add_command(search)


if __name__ == '__main__':
    cli()
