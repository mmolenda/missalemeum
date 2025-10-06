"""Shared CSS snippets for backend PDF rendering."""
from __future__ import annotations

from typing import Final

_BASE_STYLES_TEMPLATE: Final[str] = """
  @page {{
    {page_size_rule}
    margin: 15mm;
    @bottom-center {{
      content: "Page " counter(page) " / " counter(pages);
      font-size: {page_number_font_size};
      color: #555;
    }}
  }}

  * {{
    box-sizing: border-box;
  }}

  body {{
    margin: 0;
    font-family: 'Noto Serif', 'Times New Roman', serif;
    font-size: {body_font_size};
    line-height: 1.5;
    color: #000;
  }}

  h1, h2, h3, h4, h5, h6 {{
    font-weight: 600;
    page-break-after: avoid;
    page-break-inside: avoid;
    break-after: avoid;
    break-inside: avoid;
  }}

  h1 {{
    font-size: {h1_font_size};
    margin: 0 0 0.75rem;
  }}

  h2 {{
    font-size: {h2_font_size};
    margin: 1.4rem 0 0.6rem;
  }}

  h3, h4, h5, h6 {{
    font-size: {h3_font_size};
    margin: 1rem 0 0.5rem;
  }}

  p {{
    text-align: justify;
    margin: 0 0 0.6rem;
  }}

  em {{
    font-style: italic;
  }}

  .print-body {{
    padding: 0;
  }}

  .print-container {{
    min-width: 300px;
  }}

  .print-meta {{
    margin-bottom: 0.8rem;
  }}

  .print-tag {{
    display: inline-block;
    border: 1px solid #444;
    border-radius: 12px;
    padding: 0.1rem 0.6rem;
    margin: 0.1rem 0.2rem;
    font-size: {tag_font_size};
    background: #f8f8f8;
  }}

  .print-section {{
    page-break-inside: avoid;
    break-inside: avoid;
  }}

  .print-paragraph {{
    page-break-inside: avoid;
    break-inside: avoid;
    margin-bottom: 0.8rem;
  }}

  .print-paragraph:last-child {{
    margin-bottom: 0;
  }}

  .print-dual-column {{
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 0.9rem;
    page-break-inside: avoid;
    break-inside: avoid;
    align-items: stretch;
  }}

  .print-column {{
    display: flex;
    flex-direction: column;
  }}

  .print-column-content {{
    flex: 1 1 auto;
    display: flex;
    flex-direction: column;
  }}

  .print-column-content > * {{
    flex: 1 1 auto;
    display: flex;
    flex-direction: column;
  }}

  .print-column-content p {{
    flex: 1 1 auto;
    display: flex;
    align-items: flex-start;
  }}

  .print-footer {{
    text-align: center;
    margin-top: 1.2rem;
    font-size: {footer_font_size};
  }}

  .print-page-break {{
    page-break-before: always;
    break-before: page;
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


def build_bilingual_print_styles(*, page_size_rule: str, font_scale: float) -> str:
    """Return the bilingual print stylesheet scaled for the requested variant."""

    def _pt(value: float) -> str:
        return f"{value * font_scale:.2f}pt"

    return _BASE_STYLES_TEMPLATE.format(
        page_size_rule=page_size_rule,
        body_font_size=_pt(12),
        h1_font_size=_pt(22),
        h2_font_size=_pt(16),
        h3_font_size=_pt(14),
        tag_font_size=_pt(9.5),
        footer_font_size=_pt(10),
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
    )


__all__ = ["build_bilingual_print_styles"]
