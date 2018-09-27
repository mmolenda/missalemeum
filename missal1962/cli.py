#!/usr/bin/env python

import click
import datetime
import importlib
import json

from exceptions import InvalidInput
from factory import MissalFactory
from formatters.divoff import DivoffFormatter


default_language = 'Polski'


@click.group()
def cli():
    pass


@click.command()
@click.argument('year', default=datetime.datetime.utcnow().year, type=int)
@click.option('--language', default=default_language)
def calendar(year, language):
    def _print_all(missal):
        for date_, lit_day_container in missal.items():
            # if not {1, 2}.intersection(set([i.rank for i in lit_day_container.all])):
            #     continue

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


@click.command()
@click.argument('proper_id')
@click.option('--language', default=default_language)
def proper(proper_id, language):
    try:
        vernacular, latin = DivoffFormatter.run(proper_id, language)
        print(json.dumps({language: vernacular, "Latin": latin}, indent=2))
    except InvalidInput as e:
        print(e)
    except FileNotFoundError:
        print(f'No proper found for ID `{proper_id}`')


@click.command()
@click.argument('date')
@click.option('--language', default=default_language)
def date(date, language):
    yy, mm, dd = date.split('-')
    missal = MissalFactory.create(int(yy), language)
    lit_day_container = missal[datetime.date(int(yy), int(mm), int(dd))]
    print(date)
    print('tempora', [i.title for i in lit_day_container.tempora])
    print('celebration', [i.title for i in lit_day_container.celebration])


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
