"""Shared CSS snippets for backend PDF rendering."""

from __future__ import annotations

from typing import Final

_BASE_STYLES_TEMPLATE: Final[str] = """
  @import url('https://fonts.googleapis.com/css2?family=Merriweather:ital,wght@0,400;0,700;1,400;1,700&display=swap');

  @page {{
    {page_size_rule}
    margin: 12mm 10mm;
    @bottom-center {{
      content: counter(page) " / " counter(pages);
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
    font-size: {meta_font_size};
    padding-right: 0.25rem;
  }}

  .print-meta span.print-meta-separator {{
    color: #CCC;  /* same as fold_markers */
  }}

  .przeorat-block {{
    page-break-before: always;
    position: relative;
    bottom: 0;
  }}

  .przeorat-block > ul {{
    list-style: none;
    margin: 0;
    padding: 0;
  }}

  .przeorat-block > ul > li {{
    display: flex;
    align-items: center;  
    padding-bottom: 0.3em;
  }}

  .przeorat-block > ul > li::after {{
    content: "";
    flex: 1 1 auto;  
    border-bottom: 2px dotted #999;
    margin-left: 10px;
  }}

  .calendar-month {{
    margin-bottom: 1.2rem;
  }}

  .calendar-month-heading {{
    margin-top: 0;
    margin-bottom: 0.5rem;
    break-before: page;
    page-break-before: always;
  }}

  .calendar-month-heading-first {{
    break-before: auto;
    page-break-before: auto;
  }}

  .calendar-month-list {{
    margin: 0;
    padding-left: 1.2rem;
  }}

"""


def build_bilingual_print_styles(
    *, page_size: str, font_scale: float, site_label: str
) -> str:
    """Return the bilingual print stylesheet scaled for the requested variant."""

    def _pt(value: float) -> str:
        return f"{value * font_scale:.2f}pt"

    safe_site_label = str(site_label).replace('"', '\\"')

    return _BASE_STYLES_TEMPLATE.format(
        page_size_rule=f"size: {page_size};",
        body_font_size=_pt(10),
        h1_font_size=_pt(16),
        h2_font_size=_pt(12),
        meta_font_size=_pt(11),
        page_number_font_size=_pt(10),
        site_label=safe_site_label,
    )


__all__ = ["build_bilingual_print_styles"]
