import logging
import os
import sys

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from api.version import __version__
from api.apiv3 import router as apiv3_router
from api.apiv5 import router as apiv5_router

no_cache = bool(os.environ.get('MISSAL_NO_CACHE'))

logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format='[%(asctime)s ] %(levelname)s in %(module)s: %(message)s'
)


app = FastAPI(title="Missale Meum API", version=__version__)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://latinmasshelper.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.middleware("http")
async def add_cache_header(request: Request, call_next):
    response = await call_next(request)
    if not no_cache:
        response.headers.setdefault("Cache-Control", "public, max-age=604800")
    return response


app.include_router(apiv3_router)
app.include_router(apiv5_router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
