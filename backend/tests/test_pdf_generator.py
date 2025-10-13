from __future__ import annotations

from io import BytesIO

from pypdf import PdfReader
import pytest

from api.constants import TRANSLATION
from api.schemas import Proper, ProperInfo
from pdf import render as generator
from pdf.render import generate_pdf


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
    response = generate_pdf(payload=_build_payload(), variant="a4", format_hint="pdf", request_path="/tests")

    assert response.filename == "test-proper.pdf"
    assert response.pdf_bytes.startswith(b"%PDF")
    assert len(response.pdf_bytes) > 500


def test_generate_pdf_handles_unknown_variant():
    response = generate_pdf(payload=_build_payload(), variant="unknown", format_hint="pdf", request_path="/tests")

    assert response.filename.endswith(".pdf")
    assert response.pdf_bytes.startswith(b"%PDF")


@pytest.mark.parametrize("variant", ["a4-2up", "letter-2up"])
def test_generate_pdf_two_up_variant_landscape_pages(variant):
    response = generate_pdf(payload=_build_payload(), variant=variant, format_hint="pdf", request_path="/tests")

    reader = PdfReader(BytesIO(response.pdf_bytes))
    assert len(reader.pages) >= 1
    first_page = reader.pages[0]
    width = float(first_page.mediabox.width)
    height = float(first_page.mediabox.height)
    assert width > height  # landscape orientation expected for 2-up sheets


@pytest.mark.parametrize("variant", ["a4-booklet", "letter-booklet"])
def test_generate_pdf_booklet_produces_even_page_count(variant):
    response = generate_pdf(payload=_build_payload(), variant=variant, format_hint="pdf", request_path="/tests")

    reader = PdfReader(BytesIO(response.pdf_bytes))
    assert len(reader.pages) % 2 == 0
    first_page = reader.pages[0]
    assert float(first_page.mediabox.width) > float(first_page.mediabox.height)


def test_booklet_variant_contains_fold_markers():
    response = generate_pdf(payload=_build_payload(), variant="a4-booklet", format_hint="pdf", request_path="/tests")

    reader = PdfReader(BytesIO(response.pdf_bytes))
    first_page = reader.pages[0]
    contents = first_page.get_contents()
    if contents is None:
        stream = b""
    else:
        try:
            stream = contents.get_data()
        except AttributeError:
            stream = b"".join(part.get_data() for part in contents)

    assert b"0.9 0.9 0.9 RG" in stream


def test_generate_pdf_accepts_schema_objects():
    payload = [Proper.model_validate(item) for item in _build_payload()]

    response = generate_pdf(payload=payload, variant="a4", format_hint="pdf", request_path="/tests")

    assert response.filename == "test-proper.pdf"
    assert response.pdf_bytes.startswith(b"%PDF")


def test_generate_pdf_letter_variant_uses_letter_page_size():
    response = generate_pdf(payload=_build_payload(), variant="letter", format_hint="pdf", request_path="/tests")

    reader = PdfReader(BytesIO(response.pdf_bytes))
    first_page = reader.pages[0]
    width = float(first_page.mediabox.width)
    height = float(first_page.mediabox.height)
    assert height > width  # portrait orientation
    assert width == pytest.approx(612, rel=0.02)
    assert height == pytest.approx(792, rel=0.02)


def test_build_content_uses_localised_labels_for_polish():
    item = Proper.model_validate({
        "info": {
            "title": "Test",
            "date": "2024-06-01",
            "rank": 2,
            "colors": ["w", "g"],
        },
        "sections": [],
    })

    content = generator._build_content(item, "pl")

    assert content.lang == "pl"
    assert "sobota, 1 czerwca 2024" in content.meta_tags
    assert "2 klasy" in content.meta_tags
    assert "Szaty białe" in content.meta_tags
    assert "Szaty zielone" in content.meta_tags


def test_collect_meta_tags_falls_back_to_english_labels():
    info = ProperInfo.model_validate({
        "title": "Example",
        "date": "2024-06-01",
        "rank": 2,
        "colors": ["w"],
    })

    tags = generator._collect_meta_tags(info, TRANSLATION["en"])

    assert "2nd class" in tags
    assert "White vestments" in tags
    assert "Saturday, 1 June 2024" in tags


def test_wrap_html_uses_localised_page_label_and_site_url():
    html = generator._wrap_html(
        "<div></div>",
        page_size="A4",
        font_scale=1.0,
        title="Test",
        lang="pl",
    )

    assert "www.missalemeum.com" in html


def test_sanitize_custom_label_accepts_polish_letters():
    sanitized = generator._sanitize_custom_label(" Święto Pańskie-2024 ")

    assert sanitized == "Święto Pańskie-2024"


def test_sanitize_custom_label_rejects_invalid_values():
    assert generator._sanitize_custom_label("bad!") is None
    assert generator._sanitize_custom_label("abc") is None  # too short
    assert generator._sanitize_custom_label("x" * 70) is None  # too long


def test_inject_custom_label_inserts_label_first():
    contents = generator._normalise_payload(_build_payload(), lang="en")
    updated = generator._inject_custom_label(contents, "Custom Label")

    assert updated[0].meta_tags[0] == "Custom Label"
    assert list(updated[0].meta_tags)[1:] == list(contents[0].meta_tags)
