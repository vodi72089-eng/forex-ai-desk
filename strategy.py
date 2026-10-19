from pathlib import Path


def extract_pdf_text(path: Path) -> str:
    """Extract selectable text from a PDF with actionable errors for common failures."""
    from pypdf import PdfReader
    from pypdf.errors import PdfReadError

    if not path.exists():
        raise FileNotFoundError(f"Le fichier PDF est introuvable : {path}")
    if path.suffix.lower() != ".pdf":
        raise ValueError("Le fichier sélectionné n'est pas un PDF.")
    try:
        reader = PdfReader(str(path), strict=False)
    except (PdfReadError, OSError, ValueError) as exc:
        raise ValueError(f"Impossible de lire ce PDF. Le fichier est peut-être endommagé : {exc}") from exc

    if reader.is_encrypted:
        try:
            decrypted = reader.decrypt("")
        except Exception as exc:
            raise ValueError("Ce PDF est protégé par mot de passe. Déverrouille-le puis importe-le à nouveau.") from exc
        if not decrypted:
            raise ValueError("Ce PDF est protégé par mot de passe. Déverrouille-le puis importe-le à nouveau.")

    pages: list[str] = []
    for index, page in enumerate(reader.pages, start=1):
        try:
            text = page.extract_text() or ""
        except Exception as exc:
            raise ValueError(f"Erreur lors de l'extraction de la page {index} : {exc}") from exc
        if text.strip():
            pages.append(f"\n[Page {index}]\n{text.strip()}")
    return "\n".join(pages).strip()
