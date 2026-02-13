"""Resolve backend version from installed package metadata.

Falls back to the SCM-generated module and then to a static default for local
execution contexts where package metadata is unavailable.
"""

from __future__ import annotations

from importlib.metadata import PackageNotFoundError, version as package_version

PACKAGE_NAME = "missalemeum-backend"


try:
    __version__ = package_version(PACKAGE_NAME)
except PackageNotFoundError:
    try:
        from api._version import version as __version__
    except Exception:
        __version__ = "0.0.0"
