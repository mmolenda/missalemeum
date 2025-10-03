export const BILINGUAL_PRINT_STYLES = `
  @page {
    margin: 15mm;
  }

  * {
    box-sizing: border-box;
  }

  body {
    margin: 0;
    font-family: 'Noto Serif', 'Times New Roman', serif;
    font-size: 12pt;
    line-height: 1.5;
    color: #000;
  }

  h1, h2, h3, h4, h5, h6 {
    font-weight: 600;
    page-break-after: avoid;
    page-break-inside: avoid;
    break-after: avoid;
    break-inside: avoid;
  }

  h1 {
    font-size: 22pt;
    margin: 0 0 0.75rem;
  }

  h2 {
    font-size: 16pt;
    margin: 1.4rem 0 0.6rem;
  }

  h3, h4, h5, h6 {
    font-size: 14pt;
    margin: 1rem 0 0.5rem;
  }

  p {
    text-align: justify;
    margin: 0 0 0.6rem;
  }

  em {
    font-style: italic;
  }

  .print-body {
    padding: 0;
  }

  .print-container {
    min-width: 300px;
  }

  .print-meta {
    margin-bottom: 0.8rem;
  }

  .print-section {
    page-break-inside: avoid;
    break-inside: avoid;
  }

  .print-paragraph {
    page-break-inside: avoid;
    break-inside: avoid;
    margin-bottom: 0.8rem;
  }

  .print-paragraph:last-child {
    margin-bottom: 0;
  }

  .print-dual-column {
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 0.9rem;
    page-break-inside: avoid;
    break-inside: avoid;
    align-items: stretch;
  }

  .print-column {
    display: flex;
    flex-direction: column;
  }

  .print-column-content {
    flex: 1 1 auto;
    display: flex;
    flex-direction: column;
  }

  .print-column-content > * {
    flex: 1 1 auto;
    display: flex;
    flex-direction: column;
  }

  .print-column-content p {
    flex: 1 1 auto;
    display: flex;
    align-items: flex-start;
  }

  .print-footer {
    text-align: center;
    margin-top: 1.2rem;
    font-size: 10pt;
  }

  @media print and (max-width: 180mm) {
    body {
      font-size: 11pt;
      line-height: 1.45;
    }

    h1 {
      font-size: 19pt;
    }

    h2 { font-size: 15pt; margin: 1.2rem 0 0.55rem; }

    h3, h4, h5, h6 { font-size: 13pt; margin: 0.9rem 0 0.45rem; }
  }

  @media print and (max-width: 130mm) {
    body {
      font-size: 10pt;
      line-height: 1.4;
    }

    h1 {
      font-size: 17pt;
    }

    h2 { font-size: 13pt; margin: 1.1rem 0 0.5rem; }

    h3, h4, h5, h6 { font-size: 12pt; margin: 0.8rem 0 0.4rem; }
  }

  @media print and (max-width: 110mm) {
    body {
      font-size: 9pt;
      line-height: 1.35;
    }

    h1 {
      font-size: 15pt;
    }

    h2 { font-size: 12pt; margin: 1rem 0 0.45rem; }

    h3, h4, h5, h6 { font-size: 11pt; margin: 0.75rem 0 0.35rem; }
  }
`
