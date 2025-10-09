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
* Provides votive Masses, prayers, chants and other supplements
* Exposes calendar in iCal format
* Generates high-quality, well-styled PDF documents
* Shows everything in a slick, responsive UI

At the moment the application supports English and Polish vernacular languages. As the data for many other languages
is available in Divinum Officium, it is relatively easy to support them. Volunteers are welcome to contribute (see below). 

## API specficiation

The Missale Meum API is available free to use. You can access every aspect of the app, such as the calendar, propers, prayers, PDFs and more, programmatically.

For the OpenAPI specification, check out either [Swagger UI](https://www.missalemeum.com/docs) or [ReDoc](https://www.missalemeum.com/redoc).


## Running the application

### Prerequisites

* Python >=3.6
* node

### Installation

Clone the repository using `--recursive` switch to also fetch [divinum-officium](https://github.com/DivinumOfficium/divinum-officium)
as a submodule - it's used to display propers.

Create a virtualenv and install dependencies `pip install -r backend/requirements.txt`.

### Configuration

| Environment variable | Description |
|-----------------------|-------------|
| `MISSAL_NO_CACHE` | When set to `True`, disables in-memory `lru_cache` for `missalemeum.controller.get_calendar` and `missalemeum.controller.get_day`. |
| `API_URL` | Backend API base URL used by the application. |
| `NEXT_PUBLIC_API_URL` | Public-facing API URL exposed to the frontend build. |
| `NEXT_PUBLIC_BUILD_VERSION` | Build or commit identifier embedded in the application (used for version reporting). |
| `PDF_CACHE_DIR` | Filesystem path where rendered PDFs are cached. If unset, PDF caching is disabled. |
| `PDF_CACHE_SIZE_BYTES` | Maximum total size of the on-disk PDF cache (default: **1 GiB**). Old entries are evicted automatically when the limit is reached. |

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
$ python backend/api/cli.py calendar

# selected year
$ python backend/api/cli.py calendar 2020
```

Show Proprium Missae for a given date
```bash
$ python backend/api/cli.py date 2018-05-03
```

Show Proprium Missae for a given observance

*Observance ID can be obtained from calendar's output*
```bash
# Second Sunday of Advent
$ python backend/api/cli.py proper tempora:Adv2-0:1:v

# The Seven Dolors of the Blessed Virgin Mary
$ python backend/api/cli.py proper sancti:09-15:2:w
```

Show Proprium Missae for a given date or ID in columns format
```bash
$ python backend/api/cli.py proper-cols 2018-05-03
```

## Localization

### Backend

1. Copy folder [backend/api/constants/en](backend/api/constants/en) into `backend/api/constants/<your-lang-ISO-639-1>` and translate the files
2. Copy folder [backend/resources/divinum-officium-local/web/www/missa/English](backend/resources/divinum-officium-local/web/www/missa/English) into `backend/resources/divinum-officium-local/web/www/missa/<Your-language>` and translate the files if needed
3. Copy folder [backend/resources/ordo/en](backend/resources/ordo/en) into `backend/resources/ordo/<Your-language>` and translate the files
4. Copy folder [backend/resources/supplement/en](backend/resources/supplement/en) into `backend/resources/supplement/<Your-language>` and translate the files
5. Add mapping between your language ISO-639-1 code and [Divinum Officium language folder](https://github.com/DivinumOfficium/divinum-officium/tree/master/web/www/missa) in `LANGUAGES` in `backend/api/constants/common.py`
6. Add tests to your language version in [test_propers.py](backend/tests/test_propers.py). You can use  `generate_fixtures_for_propers_by_dates` from [backend/tests/util.py](backend/tests/util.py) to generate fixtures

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
