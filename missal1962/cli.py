#!/usr/bin/env python
import sys

import click
import datetime
import importlib
import json
import logging

from exceptions import InvalidInput, ProperNotFound
from factory import MissalFactory
from parsers import ProperParser

default_language = 'Polski'


logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s')


@click.group()
def cli():
    pass


@click.command()
@click.argument('year', default=datetime.datetime.utcnow().year, type=int)
@click.option('--language', default=default_language)
def calendar(year, language):
    def _print_all(missal):
        for date_, lit_day_container in missal.items():
            if date_.weekday() == 6:
                print("---")
            if date_.day == 1:
                print(f"\n\n=== {date_.month} ===\n")

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
            print(f"{date_.strftime('%A %Y-%m-%d').ljust(padding)} "
                  f"{te.ljust(padding)} {ce.ljust(padding)} {co.ljust(padding)}")

    missal = MissalFactory.create(year, language)
    _print_all(missal)


def _print_proper(language, proper):
    print(f'\n=== {language} ===\n')
    for section in proper.to_python():
        print(f'\n== {section["label"]} ==')
        print('\n'.join(section["body"]))


@click.command()
@click.argument('proper_id')
@click.option('--language', default=default_language)
def proper(proper_id, language):
    try:
        vernacular, latin = ProperParser.run(proper_id, language)
        _print_proper(language, vernacular)
        _print_proper('Latin', latin)
    except (InvalidInput, ProperNotFound) as e:
        sys.stderr.write(str(e))


@click.command()
@click.argument('date')
@click.option('--language', default=default_language)
def date(date, language):
    yy, mm, dd = date.split('-')
    date_object = datetime.date(int(yy), int(mm), int(dd))
    missal = MissalFactory.create(date_object.year, language)
    lit_day_container = missal[date_object]
    vernacular, latin = lit_day_container.get_proper()
    print(f'=== {date} ===')
    print('tempora:', lit_day_container.get_tempora_name())
    print('celebration:', lit_day_container.get_celebration_name())
    print(vernacular.to_python()[0]['body'][0])
    _print_proper(language, vernacular)
    _print_proper('Latin', latin)

@click.command()
@click.argument('search_string')
@click.option('--language', default=default_language)
def search(search_string, language):
    titles = importlib.import_module(f'resources.{language}.translation')
    for id_, title in titles.titles.items():
        if search_string.strip().lower() in title.lower():
            print(':'.join(id_.split(':')[:2]), title)


cli.add_command(calendar)
cli.add_command(date)
cli.add_command(proper)
cli.add_command(search)


if __name__ == '__main__':
    cli()
