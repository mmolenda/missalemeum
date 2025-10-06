from __future__ import annotations

from api.pdf.generator import generate_pdf


def _build_payload() -> list[dict[str, object]]:
    return [
        {
            "info": {
                "title": "Test Proper",
                "date": "2024-06-01",
                "tempora": "Ascension Octave",
                "rank": 2,
                "colors": ["w", "g"],
                "tags": ["Tag One", "Tag Two"],
                "commemorations": ["St. Justin"],
                "description": "*Introductory* description",
            },
            "sections": [
                {
                    "label": "Introitus",
                    "body": [
                        [
                            "*Psalmus 46:7*\\nSing praises to God, sing praises.",
                            "*Psalmus 46:7*\\nPsallite Deo, psallite.",
                        ],
                        [
                            "Oratio\\nO God, who has raised...",
                        ],
                    ],
                }
            ],
        }
    ]


def test_generate_pdf_produces_document():
    response = generate_pdf(payload=_build_payload(), variant="a4", format_hint="pdf")

    assert response.media_type == "application/pdf"
    disposition = response.headers.get("Content-Disposition", "")
    assert disposition.startswith("attachment; filename=\"test-proper.pdf\"")
    assert response.body.startswith(b"%PDF")
    assert len(response.body) > 500


def test_generate_pdf_handles_unknown_variant():
    response = generate_pdf(payload=_build_payload(), variant="unknown", format_hint="pdf")

    assert response.media_type == "application/pdf"
    assert response.body.startswith(b"%PDF")
