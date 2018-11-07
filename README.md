# Missal 1962

1962 Roman Catholic Missal for the Traditional Latin Mass

## Features 

* Calculate the calendar for given liturgical year
* Show Proprium Missae for given date
* Show Proprium Missae for given observance
* Search for the observances containing given word in the title

At the moment the only supported language is Polish.

## Installation

Prerequisites:

* Python 3
* [Pipenv](https://pipenv.readthedocs.io/en/latest/)

As of now the only way to install is by cloning the repository. Use `--recursive` switch
to also fetch [divinum-officium](https://github.com/DivinumOfficium/divinum-officium) as 
a submodule - it's used to display propers.

Once cloned, go to the project's dir and call `pipenv install` to install a dedicated virtualenv with
required dependencies. Then `pipenv shell` to activate the environment.

## Usage

### Command line (CLI)

Calculate the calendar
```bash
# current year
$ python missal1962/cli.py calendar

# selected year
$ python missal1962/cli.py calendar 2020
```

Show Proprium Missae for given date
```bash
$ python missal1962/cli.py date 2018-05-03
```

Show Proprium Missae for given observance

*Observance ID can be obtained either from calendar or from search command's output*
```bash
# Second Sunday of Advent
$ python missal1962/cli.py proper tempora:Adv2-0

# The Seven Dolors of the Blessed Virgin Mary
$ python missal1962/cli.py proper sancti:09-15
```

## Dev info

`kalendar.factory.MissalFactory#create` instantiates and builds `kalendar.models.Calendar` object.

`kalendar.models.Calendar` internally keeps the data in an ordered dict where a key is a `datetime.date` object, and the
value is an instance of `kalendar.models.Day` class.

Each `kalendar.models.Day` contains three list properties, `tempora`, `celebration` and `commemoration`, each one 
containing `kalendar.models.Observance` objects, representing given observance. `tempora` refers to the liturgical
time, such as "The first Friday after Pentecost", `celebration` holds `kalendar.models.Observance`s that are actually
celebrated in given day, such as "Assumption of Mary". `commemoration` contains objects representing observances
that should be commemorated with the main celebration.  

Each `kalendar.models.Day` has method `get_proper`, which calculates the actual readings in vernacular and Latin for given
calendar day. 

Each `kalendar.models.Observance` has method `get_proper`, which returns the readings for the given observance (regardless
of its place in the calendar).
