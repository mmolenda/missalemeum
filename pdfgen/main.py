
import os

from weasyprint import HTML


HERE = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(HERE, "input.html")) as fh:
    html_document = fh.read()
    base_pdf_bytes = HTML(string=html_document).write_pdf()
    with open(os.path.join(HERE, "document.pdf"), "wb") as fh:
        fh.write(base_pdf_bytes)
