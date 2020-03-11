# Missal 1962

1962 Roman Catholic Missal for the Traditional Latin Mass.

The application consists of Python/Flask API, serving calendar and propers for a given day, and Bootstrap UI consuming 
and presenting the data. The application utilizes data files from
 [Divinum Officium](https://github.com/DivinumOfficium/divinum-officium), which is linked through a
 [git submodule](./resources).

## Features 

* Calculates the 1962 calendar for given liturgical year
* Shows Proprium Missae (variable parts of the Mass) for a given date
* Provides Ordo Missae (fixed parts of the Mass)
* Exposes calendar in iCal format
* Shows everything in a slick, responsive UI

At the moment the application supports English and Polish vernacular languages. As the data for many other languages
is available in Divinum Officium, it is relatively easy to support them. Volunteers are welcome to contribute (see below). 

## Running the application

### Prerequisites:

* Python >=3.6
* [Pipenv](https://pipenv.readthedocs.io/en/latest/)

### Installation

Clone the repository using `--recursive` switch to also fetch [divinum-officium](https://github.com/DivinumOfficium/divinum-officium)
as a submodule - it's used to display propers.

Once cloned, go to the project's dir and call `pipenv install --dev` to install a dedicated virtualenv with
required dependencies. Then `pipenv shell` to activate the environment.

### Configuration

By default the application is using `lru_cache` to cache responses from `missal1962.controller` functions (which are
used by `missal1962.api` to fetch the data).

To disable caching one need to set environment variable `MISSAL_NO_CACHE` to `True`

### Run the development API:

```bash
$ python missal1962/app.py
```

and navigate to http://0.0.0.0:5000/.

## API endpoints:

Supported languages (`{lang}`): `en`, `pl`

* `GET {lang}/api/v3/calendar/{year}` get calendar for the whole year in format YYYY, e.g. "2018"
* `GET {lang}/api/v3/date/{date}` get proper for given date in format YYYY-MM-DD, e.g. "2018-05-03"
* `GET {lang}/api/v3/proper/{proper_id}` get proper for given observance by ID, regardless of its place in the calendar; 
ID can be found in response from `/calendar` endpoint, e.g. "sancti:12-24:1:v" for Nativity Vigil or "tempora:Adv4-0:1:v"
for fourth Advent Sunday 
* `GET {lang}/api/v3/icalendar/{rank}` get the calendar in iCalendar format, which can be imported to any calendar software 
such as Google Calendar. `rank` (optional, default 2) tells feast of which class to include 
(e.g. rank 3 will include classes 1, 2 and 3).    
* `GET /static/data/{lang}/ordo.json` get invariable texts, or ordinary of the Mass    

## Docker

Docker setup copies only the necessary files from Divinum Officium to keep the image light and serves the application using Gunicorn.

```bash
$ docker build -t missal1962 .
$ docker run -d -p 8000:8000 missal1962

```

and navigate to http://0.0.0.0:8000/.

## Command line (CLI)

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

*Observance ID can be obtained from calendar's output*
```bash
# Second Sunday of Advent
$ python missal1962/cli.py proper tempora:Adv2-0:1:v

# The Seven Dolors of the Blessed Virgin Mary
$ python missal1962/cli.py proper sancti:09-15:2:w
```

## Localization

1. Copy folder `missal1962/constants/en` into `missal1962/constants/<your-lang-ISO-639-1>` and translate the files
2. Add mapping between your language ISO-639-1 code and [Divinum Officium language folder](https://github.com/DivinumOfficium/divinum-officium/tree/master/web/www/missa) in `DIVOFF_LANG_MAP` in `missal1962/constants/common.py`
3. Add language mapping for Babel in `missal1962/settings.py`
4. Generate Babel language files:
    - Create .po file: `cd Missal1962/missal1962 && pybabel init -i messages.pot -d translations -l <your-lang-ISO-639-1>`
    - Provide translations in file generated in `missal1962/translations/<your-lang>/LC_MESSAGES/messages.po`
    - Compile babel files: `pybabel compile -d translations`
5. Copy folder `missal1962/templates/en` into `missal1962/templates/<your-lang-ISO-639-1>` and translate the files
5. Copy folder `missal1962/static/data/en` into `missal1962/static/data/<your-lang-ISO-639-1>` and translate the files
5. Copy folder `missal1962/static/js/en` into `missal1962/static/js/<your-lang-ISO-639-1>` and translate the files
6. Add your language dropdown in `missal1962/templates/base.html` in `ul class="navbar-nav dropdown dropdown-menu-right`
7. Run the application and verify everything is being displayed properly. Check at least one full year from now. Most likely you'll encounter some issues with Divinum Officium source files. In such case correct them in Divinum Officium project and update the submodule. 
8. Add source files for non-regular Masses, like Ash Wednesday or Maundy Thursday in `resources/divinum-officium-custom/web/www/missa/<your-lang>`


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
