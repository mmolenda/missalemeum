from __future__ import annotations

from io import BytesIO

from pypdf import PdfReader

from api.constants import TRANSLATION
from api.pdf import generator
from api.pdf.generator import generate_pdf
from api.schemas import Proper, ProperInfo


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


def test_generate_pdf_two_up_variant_landscape_pages():
    response = generate_pdf(payload=_build_payload(), variant="a4-2pages", format_hint="pdf")

    reader = PdfReader(BytesIO(response.body))
    assert len(reader.pages) >= 1
    first_page = reader.pages[0]
    width = float(first_page.mediabox.width)
    height = float(first_page.mediabox.height)
    assert width > height  # landscape orientation expected for 2-up sheets


def test_generate_pdf_booklet_produces_even_page_count():
    response = generate_pdf(payload=_build_payload(), variant="a4-booklet", format_hint="pdf")

    reader = PdfReader(BytesIO(response.body))
    assert len(reader.pages) % 2 == 0
    first_page = reader.pages[0]
    assert float(first_page.mediabox.width) > float(first_page.mediabox.height)


def test_booklet_variant_contains_fold_markers():
    response = generate_pdf(payload=_build_payload(), variant="a4-booklet", format_hint="pdf")

    reader = PdfReader(BytesIO(response.body))
    first_page = reader.pages[0]
    contents = first_page.get_contents()
    if contents is None:
        stream = b""
    else:
        try:
            stream = contents.get_data()
        except AttributeError:
            stream = b"".join(part.get_data() for part in contents)

    assert b"0.8 0.8 0.8 RG" in stream


def test_generate_pdf_accepts_schema_objects():
    payload = [Proper.model_validate(item) for item in _build_payload()]

    response = generate_pdf(payload=payload, variant="a4", format_hint="pdf")

    assert response.media_type == "application/pdf"
    assert response.body.startswith(b"%PDF")


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

    assert "Strona " in html
    assert "www.missalemeum.com" in html
