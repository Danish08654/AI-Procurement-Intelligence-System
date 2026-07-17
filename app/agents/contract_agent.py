from pypdf import PdfReader


def analyze_contract(file):

    try:

        reader = PdfReader(file)

        text = ""

        for page in reader.pages:
            text += page.extract_text() or ""

        return {
            "contract_length": len(text),
            "summary": text[:500]
        }

    except Exception as e:

        return {
            "error": str(e)
        }