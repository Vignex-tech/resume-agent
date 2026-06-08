from pypdf import PdfReader

class doc_reader():
    def read_pdf(path):
        reader = PdfReader(path)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text
    def extract_bullets(resume_text):
        pieces = resume_text.split("•")

        bullets = []
        for i, piece in enumerate(pieces):
            cleaned = " ".join(piece.split())

            if i == 0:          # the first piece is all the header gunk
                continue        # (name, contact, skills, education) — skip it
            if len(cleaned) < 30:   # guard against tiny/empty fragments
                continue

            bullets.append(cleaned)

        return bullets


# 