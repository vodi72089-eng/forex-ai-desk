from pathlib import Path


def extract_pdf_text(path: Path) -> str:
    """Extract selectable text from a PDF. OCR for scanned PDFs is not included yet."""
    from pypdf import PdfReader

    reader = PdfReader(str(path))
    pages: list[str] = []
    for index, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""
        if text.strip():
            pages.append(f"\n[Page {index}]\n{text.strip()}")
    return "\n".join(pages).strip()
