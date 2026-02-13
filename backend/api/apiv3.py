import logging
import sys

from fastapi import APIRouter, Depends
from fastapi.responses import RedirectResponse

from api.apiv5 import validate_locale

logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format='[%(asctime)s ] %(levelname)s in %(module)s: %(message)s')


router = APIRouter()


@router.get('/{lang}/api/v3/icalendar', deprecated=True)
@router.get('/{lang}/api/v3/icalendar/{rank}', deprecated=True)
def v3_ical(rank: int = 2, lang: str = Depends(validate_locale)) -> RedirectResponse:
    location = f"/{lang}/api/v5/icalendar"
    if rank:
        location += f"/{rank}"
    return RedirectResponse(url=location, status_code=302)


# Backwards compatibility for modules that still import `api`.
api = router
