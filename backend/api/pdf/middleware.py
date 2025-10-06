"""Middleware that converts JSON responses into PDFs when requested."""
from __future__ import annotations

import json
from typing import Any

from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import Response

from .decorators import is_pdf_downloadable
from .generator import generate_pdf

PDF_VARIANTS = {"a4", "a5", "a6", "a4-2pages", "a4-booklet"}
PDF_FORMAT = "pdf"


class PDFDownloadMiddleware(BaseHTTPMiddleware):
    """Intercept requests that ask for PDF output and return a static PDF stub."""

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        pdf_requested, variant_or_response = self._resolve_request_variant(request)
        if isinstance(variant_or_response, Response):
            return variant_or_response

        response = await call_next(request)

        if not pdf_requested:
            return response

        endpoint = request.scope.get("endpoint")
        if endpoint is None or not is_pdf_downloadable(endpoint):
            return response

        payload = await self._extract_payload(response)
        await self._run_background(response)

        return generate_pdf(
            payload=payload,
            variant=variant_or_response,
            format_hint=PDF_FORMAT,
            lang=request.path_params.get("lang"),
        )

    def _resolve_request_variant(self, request: Request) -> tuple[bool, Any]:
        format_param = request.query_params.get("format")
        if format_param:
            format_param = format_param.lower()
        header_accepts_pdf = self._accepts_pdf(request)
        wants_pdf = (format_param == PDF_FORMAT) or header_accepts_pdf

        if not wants_pdf:
            return False, ""

        variant_param = request.query_params.get("variant", "a4").lower()
        if variant_param not in PDF_VARIANTS:
            message = {"detail": f"Unsupported PDF variant '{variant_param}'."}
            return True, JSONResponse(status_code=400, content=message)

        return True, variant_param

    @staticmethod
    def _accepts_pdf(request: Request) -> bool:
        accept_header = request.headers.get("accept", "")
        return "application/pdf" in accept_header.lower()

    @staticmethod
    async def _extract_payload(response: Response) -> Any:
        body_bytes = await PDFDownloadMiddleware._consume_body(response)
        if not body_bytes:
            return None

        try:
            return json.loads(body_bytes)
        except json.JSONDecodeError:
            return body_bytes

    @staticmethod
    async def _consume_body(response: Response) -> bytes:
        body_chunks: list[bytes] = []
        if response.body_iterator is not None:
            async for chunk in response.body_iterator:
                body_chunks.append(chunk)
        else:
            body = getattr(response, "body", b"")
            if body:
                body_chunks.append(body)
        return b"".join(body_chunks)

    @staticmethod
    async def _run_background(response: Response) -> None:
        if response.background is not None:
            await response.background()
