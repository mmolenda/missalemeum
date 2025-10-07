"""Shared CSS snippets for backend PDF rendering."""

from __future__ import annotations

from typing import Final

_BASE_STYLES_TEMPLATE: Final[str] = """
  @import url('https://fonts.googleapis.com/css2?family=Merriweather:ital,wght@0,400;0,700;1,400;1,700&display=swap');

  @page {{
    {page_size_rule}
    margin: 15mm;
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

  h2 {{
      break-after: avoid;
      page-break-after: avoid;
      text-transform: uppercase;

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

  @media print and (max-width: 180mm) {{
    body {{
      font-size: {media_180_body_font_size};
      line-height: 1.45;
    }}

    h1 {{
      font-size: {media_180_h1_font_size};
    }}

    h2 {{ font-size: {media_180_h2_font_size}; margin: 1.2rem 0 0.55rem; }}

    h3, h4, h5, h6 {{ font-size: {media_180_h3_font_size}; margin: 0.9rem 0 0.45rem; }}
  }}

  @media print and (max-width: 130mm) {{
    body {{
      font-size: {media_130_body_font_size};
      line-height: 1.4;
    }}

    h1 {{
      font-size: {media_130_h1_font_size};
    }}

    h2 {{ font-size: {media_130_h2_font_size}; margin: 1.1rem 0 0.5rem; }}

    h3, h4, h5, h6 {{ font-size: {media_130_h3_font_size}; margin: 0.8rem 0 0.4rem; }}
  }}

  @media print and (max-width: 110mm) {{
    body {{
      font-size: {media_110_body_font_size};
      line-height: 1.35;
    }}

    h1 {{
      font-size: {media_110_h1_font_size};
    }}

    h2 {{ font-size: {media_110_h2_font_size}; margin: 1rem 0 0.45rem; }}

    h3, h4, h5, h6 {{ font-size: {media_110_h3_font_size}; margin: 0.75rem 0 0.35rem; }}
  }}
"""


def build_bilingual_print_styles(
    *, page_size_rule: str, font_scale: float, page_label: str, site_label: str
) -> str:
    """Return the bilingual print stylesheet scaled for the requested variant."""

    def _pt(value: float) -> str:
        return f"{value * font_scale:.2f}pt"

    safe_page_label = str(page_label).replace('"', '\\"')
    safe_site_label = str(site_label).replace('"', '\\"')

    return _BASE_STYLES_TEMPLATE.format(
        page_size_rule=page_size_rule,
        body_font_size=_pt(12),
        h1_font_size=_pt(22),
        h2_font_size=_pt(16),
        h3_font_size=_pt(14),
        meta_font_size=_pt(10),
        page_number_font_size=_pt(9),
        media_180_body_font_size=_pt(11),
        media_180_h1_font_size=_pt(19),
        media_180_h2_font_size=_pt(15),
        media_180_h3_font_size=_pt(13),
        media_130_body_font_size=_pt(10),
        media_130_h1_font_size=_pt(17),
        media_130_h2_font_size=_pt(13),
        media_130_h3_font_size=_pt(12),
        media_110_body_font_size=_pt(9),
        media_110_h1_font_size=_pt(15),
        media_110_h2_font_size=_pt(12),
        media_110_h3_font_size=_pt(11),
        page_label=safe_page_label,
        site_label=safe_site_label,
    )


__all__ = ["build_bilingual_print_styles"]
