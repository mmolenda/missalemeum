# Missal 1962

1962 Roman Catholic Missal for the Traditional Latin Mass.

The application consists of Python/Flask API, serving calendar and propers for a given day, and Bootstrap UI consuming 
and presenting the data. The application utilizes data files from
 [Divinum Officium](https://github.com/DivinumOfficium/divinum-officium), which is linked through a
 [git submodule](./resources).

## Features 

* Calculates the calendar for given liturgical year
* Shows Proprium Missae for a given date
* Shows Proprium Missae for a given observance

At the moment the only supported vernacular language is Polish, but since the data for many other languages
is available in Divinum Officium, it will be relatively easy to support them. Volunteers are welcome to contribute. 

## Running the application

### API mode

#### Prerequisites:

* Python 3.6
* [Pipenv](https://pipenv.readthedocs.io/en/latest/)

#### Installation

Clone the repository using `--recursive` switch to also fetch [divinum-officium](https://github.com/DivinumOfficium/divinum-officium)
as a submodule - it's used to display propers.

Once cloned, go to the project's dir and call `pipenv install --dev` to install a dedicated virtualenv with
required dependencies. Then `pipenv shell` to activate the environment.

#### Configuration

In [index.html](missal1962/static/index.html) change js config link from `js/conf-static.js` to `js/conf-api.js`.

By default the application is using `lru_cache` to cache responses from `missal1962.controller` functions (which are
used by `missal1962.api` to fetch the data).

To disable caching one need to set environment variable `MISSAL_NO_CACHE` to `True`

#### Run the development API:

```bash
$ python missal1962/api.py
```

and navigate to http://0.0.0.0:5000/.

#### API endpoints:

* `GET /` serve the static files 
* `GET /calendar/{year}` get calendar for the whole year in format YYYY, e.g. "2018"
* `GET /date/{date}` get proper for given date in format YYYY-MM-DD, e.g. "2018-05-03"
* `GET /proper/{proper_id}` get proper for given observance by ID, regardless of its place in the calendar; ID can be found in response from `/calendar` endpoint, e.g. "sancti:12-24" for Nativity Vigil or "tempora:Adv4-0" for fourth Advent Sunday 


### Docker

Docker setup spins up the application in the API mode.
It copies only the necessary files from Divinum Officium to keep the image light and serves the application using Gunicorn.

```bash
$ docker build -t missal1962 .
$ docker run -d -p 8000:8000 missal1962

```

and navigate to http://0.0.0.0:8000/.

### Static mode

The application can also work without the API. In such a case it utilizes a limited set of [generated data files](missal1962/static/data).

To run in this mode simply navigate to [static](missal1962/static) directory and serve the content using any http server, for example:

```bash
$ cd missal1962/static
$ python -m http.server 8080
```

and navigate to http://0.0.0.0:8080/.

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

*Observance ID can be obtained from calendar's output*
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
