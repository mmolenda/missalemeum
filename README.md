# Missale Meum

1962 Roman Catholic Missal for the Traditional Latin Mass.

The application consists of Python/Flask API, serving calendar and propers for a given day, and Nextjs/React frontend consuming 
and presenting the data. The application utilizes data files from
 [Divinum Officium](https://github.com/DivinumOfficium/divinum-officium), which is linked through a
 [git submodule](./backend/resources).

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

Create a virtualenv and install dependencies `pip install -r backend/requirements.txt`.

### Configuration

By default the application is using `lru_cache` to cache responses from `missalemeum.controller` functions (which are
used by `missalemeum.api` to fetch the data).

To disable caching one need to set environment variable `MISSAL_NO_CACHE` to `True`

Backend API URL needs to be provided in `API_URL` env variable.

Application build version is provided in `NEXT_PUBLIC_BUILD_VERSION` env variable.

### Run the python development API

```bash
$ export PYTHONPATH=$PYTHONPATH:backend
$ python backend/api/app.py
```

and navigate to http://0.0.0.0:8000/en/api/v5/version.

### Run the nextjs development UI

Provide local dev API URL in variable `API_URL`:

```bash
export API_URL=http://localhost:8000
```

Navigate to `./frontend`

```
npm ci
npm run dev
```

and navigate to http://0.0.0.0:3000.

## API specficiation

See [openapi.yaml](openapi.yaml) or [auto-generated swagger API documentation](https://editor.swagger.io/?url=https://raw.githubusercontent.com/mmolenda/missalemeum/master/openapi.yaml) based on the latter.     

## Docker

Docker compose setup for this project runs three containers - backend, frontend and caddy server as a reverse proxy.

```bash
$ docker compose up --build
```

and navigate to http://0.0.0.0:8000/.

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

1. Copy folder [backend/api/constants/en](backend/api/constants/en) into `backend/api/constants/<your-lang-ISO-639-1>` and translate the files
2. Copy folder [backend/resources/divinum-officium-local/web/www/missa/English](backend/resources/divinum-officium-local/web/www/missa/English) into `backend/resources/divinum-officium-local/web/www/missa/<Your-language>` and translate the files if needed
3. Add mapping between your language ISO-639-1 code and [Divinum Officium language folder](https://github.com/DivinumOfficium/divinum-officium/tree/master/web/www/missa) in `LANGUAGES` in `backend/api/constants/common.py`
4. Add tests to your language version in [test_propers.py](backend/tests/test_propers.py). You can use  `generate_fixtures_for_propers_by_dates` from [backend/tests/util.py](backend/tests/util.py) to generate fixtures

### Frontend

1. Add languages and translations in [frontend/components/intl.tsx](frontend/components/intl.tsx)

### Verification

Run the application and verify everything is being displayed properly. Check at least one full year from now. Most likely you'll encounter 
some issues with Divinum Officium source files. In such case correct them in [backend/resources/divinum-officium-local](backend/resources/divinum-officium-local).

[backend/resources/divinum-officium-local](backend/resources/divinum-officium-local) serves as an intermediary data layer between Missale Meum and Divinum Officium to 
separate MM from DF complexities (stemming from multiple missal versions, not too clean code and hectic changes). For 
simplicity and easier management (at cost of higher redundancy), "local" layer resolves ONLY first level references defined
inside sections. 

For example if `Sancti/11-11.txt` has

```
[Lectio]
@Commune/C4
```

It will resolve only to `Commune/C4:Lectio` and it is expected that `Commune/C4:Lectio` will contain the final text, not another reference, as it won't be resolved further. Also global referneces in target files, like for example

```
[Rule]
ex C11;
```

will not be resolved either. So each file in "local" data folder must implement all sections explicitly, except if it is a vernacular 
language, it will inherit from corresponding Latin file from "local", so for instance if English version of `Sancti/12-24.txt` has exactly 
same references as its Latin counterpart, it can and should be left empty.

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

Add `backend` directory to the `PYTHONPATH` environment variable and use `pytest`.

Or in the root directory set an alias for `pytest`: `alias pytest="PYTHONPATH=$(pwd)/backend:$(pwd)/tests pytest"`
