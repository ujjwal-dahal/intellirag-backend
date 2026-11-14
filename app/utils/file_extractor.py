import pymupdf


def extract_pdf_text(file_bytes: bytes) -> str:
    """
    Extract text from PDF bytes using PyMuPDF.
    """

    with pymupdf.open(
        stream=file_bytes,
        filetype="pdf",
    ) as pdf:

        # Checking Password Protected PDF
        if pdf.needs_pass:
            raise ValueError("Password-protected PDFs are not supported.")

        extracted_pages = []

        for page in pdf:
            page_text = page.get_text("text")

            if page_text.strip():
                extracted_pages.append(page_text)

        text = "\n\n".join(extracted_pages).strip()

        if not text:
            raise ValueError("No extractable text found in PDF.")

        return text


def extract_txt_text(file_bytes: bytes) -> str:
    """
    Extract text from TXT file bytes.
    """

    try:
        text = file_bytes.decode("utf-8-sig").strip()

    except UnicodeDecodeError as error:
        raise ValueError("TXT file must use UTF-8 encoding.") from error

    if not text:
        raise ValueError("TXT file is empty.")

    if "\x00" in text:
        raise ValueError("Invalid text file content.")

    return text


def extract_text(
    file_bytes: bytes,
    file_type: str,
) -> str:
    """
    Extract text based on file type.
    """

    if file_type == "pdf":
        return extract_pdf_text(file_bytes)

    if file_type == "txt":
        return extract_txt_text(file_bytes)

    raise ValueError("Unsupported file type.")
