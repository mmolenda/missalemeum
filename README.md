# Missale Meum

1962 Roman Catholic Missal for the Traditional Latin Mass.

The application consists of Python/Flask API, serving calendar and propers for a given day, and React UI consuming 
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

### Prerequisites

* Python >=3.6
* node

### Installation

Clone the repository using `--recursive` switch to also fetch [divinum-officium](https://github.com/DivinumOfficium/divinum-officium)
as a submodule - it's used to display propers.

Create a virtualenv and install dependencies `pip install -r requirements.txt`.

### Configuration

By default the application is using `lru_cache` to cache responses from `missalemeum.controller` functions (which are
used by `missalemeum.api` to fetch the data).

To disable caching one need to set environment variable `MISSAL_NO_CACHE` to `True`

### Run the development API

```bash
$ python missalemeum/app.py
```

and navigate to http://0.0.0.0:8000/en/api/v5/version.

### Run the development UI

Provide local dev API URL in variable `REACT_APP_API_URL`:

```bash
export REACT_APP_API_URL=http://localhost:8000
```

Navigate to `./frontend`

```
npm install
npm run start
```

and navigate to http://0.0.0.0:3000.

## API specficiation

See [openapi.yaml](openapi.yaml) or [auto-generated swagger API documentation](https://editor.swagger.io/?url=https://raw.githubusercontent.com/mmolenda/missalemeum/master/openapi.yaml) based on the latter.     

## Docker

Docker setup for this project runs multi stage build. In the first stage an optimised production build of React UI is created. 
In the second step Docker setup copies only the necessary files from Divinum Officium to keep the image light and serves the application using Gunicorn.

```bash
$ docker build -t missalemeum .
$ docker run -d -p 8000:8000 missalemeum
```

and navigate to http://0.0.0.0:8000/.

### Running tests in Docker

Build the image.
Run `docker run missalemeum sh -c "pytest tests"`

## Command line (CLI)

Calculate the calendar
```bash
# current year
$ python missalemeum/cli.py calendar

# selected year
$ python missalemeum/cli.py calendar 2020
```

Show Proprium Missae for given date
```bash
$ python missalemeum/cli.py date 2018-05-03
```

Show Proprium Missae for given observance

*Observance ID can be obtained from calendar's output*
```bash
# Second Sunday of Advent
$ python missalemeum/cli.py proper tempora:Adv2-0:1:v

# The Seven Dolors of the Blessed Virgin Mary
$ python missalemeum/cli.py proper sancti:09-15:2:w
```

## Localization

### Backend

1. Copy folder `missalemeum/constants/en` into `missalemeum/constants/<your-lang-ISO-639-1>` and translate the files
2. Add mapping between your language ISO-639-1 code and [Divinum Officium language folder](https://github.com/DivinumOfficium/divinum-officium/tree/master/web/www/missa) in `LANGUAGES` in `missalemeum/constants/common.py`
3. Generate Babel language files:
    - Create .po file: `cd missalemeum/missalemeum && pybabel init -i messages.pot -d translations -l <your-lang-ISO-639-1>`
    - Provide translations in file generated in `missalemeum/translations/<your-lang>/LC_MESSAGES/messages.po`
    - Compile babel files: `pybabel compile -d translations`
4. Copy folder `missalemeum/templates/en` into `missalemeum/templates/<your-lang-ISO-639-1>` and translate the files
5. Add source files for non-regular propers, like Ash Wednesday or Maundy Thursday in `resources/divinum-officium-custom/web/www/missa/<your-lang>`

### Frontend

1. Add your language to `supportedLanguages` array in [App.js](frontend/src/App.js)
2. Provide translation of fronted elements in [intl.js](frontend/src/intl.js)

### Verification

Run the application and verify everything is being displayed properly. Check at least one full year from now. Most likely you'll encounter 
some issues with Divinum Officium source files. In such case correct them in Divinum Officium project and update the submodule.

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

## Tests

Add `missalemeum` and `tests` directories to the `PYTHONPATH` environment variable and use `pytest`.

Or in the root directory set an alias for `pytest`: `alias pytest="PYTHONPATH=$(pwd)/missalemeum:$(pwd)/tests pytest"`
