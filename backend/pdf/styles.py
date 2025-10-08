"""Shared CSS snippets for backend PDF rendering."""

from __future__ import annotations

from typing import Final

_BASE_STYLES_TEMPLATE: Final[str] = """
  @import url('https://fonts.googleapis.com/css2?family=Merriweather:ital,wght@0,400;0,700;1,400;1,700&display=swap');

  @page {{
    {page_size_rule}
    margin: 10mm;
    @bottom-center {{
      content: "{page_label} " counter(page) " / " counter(pages);
      font-size: {page_number_font_size};
      color: #555;
    }}
    @bottom-right {{
      content: "{site_label}";
      font-size: {page_number_font_size};
      color: #555;
    }}
  }}

  * {{
    box-sizing: border-box;
  }}

  body {{
    margin: 0;
    font-family: 'Merriweather', 'Noto Serif', 'Times New Roman', serif;
    font-size: {body_font_size};
    line-height: 1.5;
    color: #000;
  }}

  h1 {{
    font-size: {h1_font_size};
    text-align: center;
  }}

  h2 {{
      font-size: {h2_font_size};
      text-align: center;
      line-height: 0.5;
      break-after: avoid;
      page-break-after: avoid;
      text-transform: uppercase;

  }}

  p {{
    widows: 2;
    orphans: 2;
    hyphens: auto;           /* enable hyphenation */
    overflow-wrap: anywhere; /* allow emergency breaks */
    text-align: justify;     /* lets the line breaker work better */
  }}

  /* two-column bilingual layout */
  .print-dual-column {{
      display: table;
      table-layout: fixed;
      width: 100%;
      border-spacing: 0;
      margin-bottom: 0.8rem;
  }}

  .print-column {{
      display: table-cell;
      width: 50%;
      vertical-align: top;
      box-sizing: border-box;
  }}

  .print-column:first-of-type {{
      padding-right: 0.45rem;
  }}

  .print-column:last-of-type {{
      padding-left: 0.45rem;
  }}

  .print-paragraph {{
    padding-bottom: 0.5rem;
  }}

  .print-meta {{
    text-align: center;
    padding-bottom: 0.5rem;
  }}

  .print-meta > span {{
    font-style: italic;
    padding-right: 0.25rem;
  }}

  .przeorat-table {{
    width: 100%;
    margin-top: 1.2rem;
    border-collapse: collapse;
  }}

  .przeorat-table td {{
    border: 1px solid #444;
    padding: 0.4rem 0.5rem;
    vertical-align: middle;
  }}

  .przeorat-table td:first-of-type {{
    width: 33.333%;
  }}

  .przeorat-table td:last-of-type {{
    width: 66.667%;
  }}

"""


def build_bilingual_print_styles(
    *, page_size: str, font_scale: float, page_label: str, site_label: str
) -> str:
    """Return the bilingual print stylesheet scaled for the requested variant."""

    def _pt(value: float) -> str:
        return f"{value * font_scale:.2f}pt"

    safe_page_label = str(page_label).replace('"', '\\"')
    safe_site_label = str(site_label).replace('"', '\\"')

    return _BASE_STYLES_TEMPLATE.format(
        page_size_rule=f"size: {page_size};",
        body_font_size=_pt(10),
        h1_font_size=_pt(18),
        h2_font_size=_pt(12),
        meta_font_size=_pt(10),
        page_number_font_size=_pt(10),
        page_label=safe_page_label,
        site_label=safe_site_label,
    )


__all__ = ["build_bilingual_print_styles"]

