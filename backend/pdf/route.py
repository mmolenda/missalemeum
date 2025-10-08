"""Custom APIRoute that post-processes responses into PDFs when requested."""
from __future__ import annotations

import json
from typing import Any, Callable

from fastapi import Request
from fastapi.routing import APIRoute
from starlette.responses import Response as StarletteResponse

from .dependencies import get_pdf_options
from .options import (
    DEFAULT_VARIANT_CHOICE,
    MAX_CONTENT_INDEX,
    OutputFormat,
    PDF_FORMAT,
    PDF_STATE_KEY,
    PDFVariant,
    PdfOptions,
)
from .render import generate_pdf


class PDFAwareRoute(APIRoute):
    """Route that converts responses to PDF for endpoints that opt in."""

    def get_route_handler(self) -> Callable[[Request], Any]:
        original_route_handler = super().get_route_handler()
        pdf_dependency_declared = self._is_pdf_enabled()

        async def pdf_route_handler(request: Request) -> StarletteResponse:
            response: StarletteResponse = await original_route_handler(request)
            if not pdf_dependency_declared:
                return response

            options = getattr(request.state, PDF_STATE_KEY, None)
            if options is None:
                options = self._fallback_options(request)
            if not isinstance(options, PdfOptions) or not options.is_requested():
                return response

            payload = await self._extract_payload(response)
            await self._run_background(response)

            variant_key = options.variant.value if options.variant is not None else None
            format_hint = options.format_hint.value if options.format_hint is not None else PDF_FORMAT

            return generate_pdf(
                payload=payload,
                variant=variant_key or DEFAULT_VARIANT_CHOICE.value,
                format_hint=format_hint,
                lang=request.path_params.get("lang"),
                index=options.index,
                custom_label=options.custom_label,
            )

        return pdf_route_handler

    def _is_pdf_enabled(self) -> bool:
        if self.dependant is None:
            return False
        for dependency in self.dependant.dependencies:
            if dependency.call is get_pdf_options:
                return True
        return False

    @staticmethod
    async def _extract_payload(response: StarletteResponse) -> Any:
        body_bytes = await PDFAwareRoute._consume_body(response)
        if not body_bytes:
            return None
        try:
            return json.loads(body_bytes)
        except json.JSONDecodeError:
            return body_bytes

    @staticmethod
    async def _consume_body(response: StarletteResponse) -> bytes:
        body_chunks: list[bytes] = []
        body_iterator = getattr(response, "body_iterator", None)
        if body_iterator is not None:
            async for chunk in response.body_iterator:
                body_chunks.append(chunk)
        else:
            body = getattr(response, "body", b"")
            if isinstance(body, bytes):
                if body:
                    body_chunks.append(body)
            elif isinstance(body, str):
                if body:
                    body_chunks.append(body.encode(response.charset or "utf-8"))
            else:
                try:
                    materialised = await response.body()
                except TypeError:
                    materialised = b""
                if materialised:
                    body_chunks.append(materialised if isinstance(materialised, bytes) else bytes(materialised))
        return b"".join(body_chunks)

    @staticmethod
    async def _run_background(response: StarletteResponse) -> None:
        if response.background is not None:
            await response.background()

    @staticmethod
    def _fallback_options(request: Request) -> PdfOptions:
        query = request.query_params

        format_choice: OutputFormat | None
        format_param = query.get("format")
        try:
            format_choice = OutputFormat(format_param) if format_param else None
        except ValueError:
            format_choice = None

        variant_param = query.get("variant")
        try:
            variant_choice = PDFVariant(variant_param) if variant_param else DEFAULT_VARIANT_CHOICE
        except ValueError:
            variant_choice = DEFAULT_VARIANT_CHOICE

        index_param = query.get("index")
        index_value = 0
        if index_param is not None:
            try:
                index_value = int(index_param)
            except (TypeError, ValueError):
                index_value = 0
        if index_value < 0 or index_value > MAX_CONTENT_INDEX:
            index_value = 0

        custom_label = query.get("custom_label")
        requested = False
        if format_choice is not None:
            requested = format_choice is OutputFormat.PDF
        else:
            accept_header = request.headers.get("accept", "")
            if "application/pdf" in accept_header.lower():
                requested = True
                format_choice = OutputFormat.PDF

        options = PdfOptions(
            requested=requested,
            format_hint=format_choice,
            variant=variant_choice,
            index=index_value,
            custom_label=custom_label,
        )

        setattr(request.state, PDF_STATE_KEY, options)
        return options


__all__ = ["PDFAwareRoute"]
